/*
 * This code is provided solely for the personal and private use of students
 * taking the CSC369H course at the University of Toronto. Copying for purposes
 * other than this use is expressly prohibited. All forms of distribution of
 * this code, including but not limited to public repositories on GitHub,
 * GitLab, Bitbucket, or any other online platform, whether as given or with
 * any changes, are expressly prohibited.
 *
 * Authors: Alexey Khrabrov, Karen Reid, Angela Demke Brown
 *
 * All of the files in this directory and all subdirectories are:
 * Copyright (c) 2022 Angela Demke Brown
 */

/**
 * CSC369 Assignment 5 - vsfs formatting tool.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>
#include "vsfs.h"
#include "bitmap.h"
#include "map.h"

/** Command line options. */
typedef struct mkfs_opts {
	/** File system image file path. */
	const char *img_path;
	/** Number of inodes. */
	size_t n_inodes;

	/** Print help and exit. */
	bool help;
	/** Overwrite existing file system. */
	bool force;
	/** Zero out image contents. */
	bool zero;

} mkfs_opts;

static const char *help_str = "\
Usage: %s options image\n\
\n\
Format the image file into vsfs file system. The file must exist and\n\
its size must be a multiple of vsfs block size - %zu bytes.\n\
\n\
Options:\n\
    -i num  number of inodes; required argument\n\
    -h      print help and exit\n\
    -f      force format - overwrite existing vsfs file system\n\
    -z      zero out image contents\n\
";

static void print_help(FILE *f, const char *progname)
{
	fprintf(f, help_str, progname, VSFS_BLOCK_SIZE);
}


static bool parse_args(int argc, char *argv[], mkfs_opts *opts)
{
	char o;
	while ((o = getopt(argc, argv, "i:hfvz")) != -1) {
		switch (o) {
			case 'i': opts->n_inodes = strtoul(optarg, NULL, 10); break;

			case 'h': opts->help  = true; return true;// skip other arguments
			case 'f': opts->force = true; break;
			case 'z': opts->zero  = true; break;

			case '?': return false;
			default : assert(false);
		}
	}

	if (optind >= argc) {
		fprintf(stderr, "Missing image path\n");
		return false;
	}
	opts->img_path = argv[optind];

	if (opts->n_inodes == 0) {
		fprintf(stderr, "Missing or invalid number of inodes\n");
		return false;
	}
	return true;
}


/** Determine if the image has already been formatted into vsfs. */
static bool vsfs_is_present(void *image)
{
	// Check if the image already contains a valid vsfs superblock.
	// This may be overly trusting. You can add additional sanity checks.
	
	vsfs_superblock *sb = (vsfs_superblock *)image;
	if (sb->magic == VSFS_MAGIC) {
		return true;
	} else {
		return false;
	}
}


/**
 * Format the image into vsfs.
 *
 * NOTE: Must update mtime of the root directory.
 *
 * @param fd     open file descriptor for the disk image file
 * @param buf    scratch buffer of at least VSFS_BLOCK_SIZE bytes
 * @param size   image file size in bytes.
 * @param opts   command line options.
 * @return       true on success;
 *               false on error, e.g. options are invalid for given image size. 
 */
static bool mkfs(void *image, size_t size, mkfs_opts *opts)
{
	//TODO: initialize the superblock and create an empty root directory
	//NOTE: the mode of the root directory inode should be set
	//      to S_IFDIR | 0777

	vsfs_superblock *sb;       // ptr to superblock in mmap'd disk image
	bitmap_t        *ibmap;    // ptr to inode bitmap in mmap'd disk image
	bitmap_t        *dbmap;    // ptr to data block bitmap in mmap'd image
	vsfs_inode      *itable;   // ptr to inode table in mmap'd image

	vsfs_inode  *root_ino;     // ptr to root inode (in inode table)
	vsfs_dentry *root_entries; // ptr to root dir data block in mmap'd image

	// sb->size = 0;
	// sb->free_inodes = 0;
	// sb->free_blocks = 0;
	// sb->data_region = 0;
	
	vsfs_blk_t nblks = size / VSFS_BLOCK_SIZE;
	uint32_t inodes_per_block = VSFS_BLOCK_SIZE / sizeof(vsfs_inode);
	bool ret = false;
	
	if (opts->n_inodes >= VSFS_INO_MAX) {
		return false;
	}

	if (nblks > VSFS_BLK_MAX || nblks < VSFS_BLK_MIN) {
		return false;
	}

	// setting num_blocks and num_inodes attributes for superblock
	// sb->num_blocks = nblks;
	// sb->num_inodes = inodes_per_block * nblks;

	// root_ino->i_mode = S_IFDIR;
	// root_ino->i_nlink = 2;
	// root_ino->i_size = VSFS_BLOCK_SIZE;
	// // root_ino->
	// itable[VSFS_ROOT_INO] = *root_ino;

	// Initialize inode bitmap in memory (write to disk happens at munmap).
	// First set all bits to 1, then use bitmap_init to clear the bits
	// for the given number of inodes in the file system.
	
	ibmap = (bitmap_t *)(image + VSFS_IMAP_BLKNUM * VSFS_BLOCK_SIZE);	
	memset(ibmap, 0xff, VSFS_BLOCK_SIZE);
	bitmap_init(ibmap, opts->n_inodes);
	
	// Initialize data bitmap in memory (write to disk happens at munmap).
	// First set all bits to 1, then use bitmap_init to clear the bits
	// for the given number of blocks in the file system.
	
	dbmap = (bitmap_t *)(image + VSFS_DMAP_BLKNUM * VSFS_BLOCK_SIZE);
	memset(dbmap, 0xff, VSFS_BLOCK_SIZE);
	bitmap_init(dbmap, nblks);
	
	// Mark first 3 blocks (superblock, inode bitmap, data bitmap) allocated.
	bitmap_set(dbmap, nblks, VSFS_SB_BLKNUM, true); // superblock
	bitmap_set(dbmap, nblks, VSFS_IMAP_BLKNUM, true); // inode bitmap block
	bitmap_set(dbmap, nblks, VSFS_DMAP_BLKNUM, true); // data bitmap block
	
	// TODO: Calculate size of inode table and mark inode table blocks allocated.
	(void)inodes_per_block;
	int itable_length = div_round_up(opts->n_inodes, inodes_per_block);
	for(int i = 0; i < itable_length; i++){
		bitmap_set(dbmap, nblks, VSFS_ITBL_BLKNUM + i, true);
	}
	// memset(itable, 1, VSFS_BLOCK_SIZE);
	// bitmap_init(itable, itable_length);
	// uint32_t index;
	// int status = bitmap_alloc(ibmap, itable_length, &index);
	// assert(status == 0);

	// TODO: Initialize the root directory.
	// 1. Mark root directory inode allocated in inode bitmap
	// bitmap set the i bitmap
	bitmap_set(ibmap, opts->n_inodes, VSFS_SB_BLKNUM, true);

	// 2. Initialize fields of root dir inode (the mtime is done for you)
	itable = (vsfs_inode *)(image + VSFS_ITBL_BLKNUM * VSFS_BLOCK_SIZE);	
	root_ino = &itable[VSFS_ROOT_INO];
	root_ino->i_mode = S_IFDIR | 0777;
	root_ino->i_nlink = 2;
	root_ino->i_size = VSFS_BLOCK_SIZE;
	root_ino->i_blocks = 1;
	// root_ino->
	// itable[VSFS_ROOT_INO] = *root_ino;
	for(int j = 0; j < VSFS_NUM_DIRECT; j++){
		root_ino->i_direct[j] = 0;
	}
	root_ino->i_indirect = 0;

	
	if (clock_gettime(CLOCK_REALTIME, &(root_ino->i_mtime)) != 0) {
		perror("clock_gettime");
		goto out;
	}
	
	// 3. Allocate a data block for root directory; record it in root inode
	(void)root_entries;
	uint32_t i;
	int status = bitmap_alloc(dbmap, nblks, &i);
	assert(status == 0);
	root_ino->i_direct[0] = i;
	// root_entries->ino = VSFS_ROOT_INO;
	// root_ino->i_direct->ino = VSFS_ROOT_INO;
	
	// 4. Create '.' and '..' entries in root dir data block.
	int num_iblocks = div_round_up(opts->n_inodes, inodes_per_block);
	root_entries = (vsfs_dentry *)(image + i * VSFS_BLOCK_SIZE);
	root_entries[0].ino = VSFS_ROOT_INO;
	root_entries[1].ino = VSFS_ROOT_INO;
	strncpy(root_entries[0].name, ".", VSFS_NAME_MAX);
	strncpy(root_entries[1].name, "..", VSFS_NAME_MAX);
	
	// 5. Initialize other dir entries in block to invalid / unused state
	//    Since 0 is a valid inode, use VSFS_INO_MAX to indicate invalid.
	int size2 = VSFS_BLOCK_SIZE / sizeof(vsfs_dentry);
	for (int i = 2; i < size2; i++) {
		root_entries[i].ino = VSFS_INO_MAX;
	}

	// TODO: Initialize fields of superblock after everything else succeeds.
	// Set start of data region to first block after inode table.
	sb = (vsfs_superblock *)image;
	sb->data_region = num_iblocks + 3;
	sb->magic = VSFS_MAGIC;
	sb->num_blocks = nblks;
	sb->num_inodes = opts->n_inodes;
	sb->free_blocks = nblks - 4 - num_iblocks;
	sb->free_inodes = opts->n_inodes - 1;
	(void)sb;
	
	ret = true;
 out:
	return ret;
}


int main(int argc, char *argv[])
{
	int ret; // return value; 0 on success, 1 on failure
	size_t fsize; // size of disk image file 
	void *image;  // pointer to mmap'd disk image file
	mkfs_opts opts = {0}; // options; defaults are all 0
	
	if (!parse_args(argc, argv, &opts)) {
		// Invalid arguments, print help to stderr
		print_help(stderr, argv[0]);
		return 1;
	}
	
	if (opts.help) {
		// Help requested, print it to stdout
		print_help(stdout, argv[0]);
		return 0;
	}

	// Map disk image file into memory
	image = map_file(opts.img_path, VSFS_BLOCK_SIZE, &fsize);
	if (image == NULL) {
		return 1;
	}

	// Check if overwriting existing file system
	if (!opts.force && vsfs_is_present((vsfs_superblock *)image)) {
		fprintf(stderr, "Image already contains vsfs; use -f to overwrite\n");
		goto end;
	}

	if (opts.zero) {
		// Fill buffer with zeros
		memset(image, 0, fsize);
	}
	
	if (!mkfs(image, fsize, &opts)) {
		fprintf(stderr, "Failed to format the image\n");
		goto end;
	}

	ret = 0;
	
end:
	munmap(image, fsize);
	return ret;
}
