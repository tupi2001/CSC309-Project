import {createContext, useState} from "react";

export const useAPIContext = () => {
    const [classes, setClasses] = useState([]);

    return {
        classes,
        setClasses,
    }
}

const APIContext = createContext({
    classes: null, setClasses: () => {},
})

export default APIContext;