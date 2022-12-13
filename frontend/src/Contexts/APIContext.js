
import {createContext, useState} from "react";

export const useAPIContext = () => {
    const [gymclasses, setClasses] = useState([]);

    return {
        gymclasses,
        setClasses,
    }
}

const APIContext = createContext({
    gymclasses: null, setClasses: () => {},
})

export default APIContext;