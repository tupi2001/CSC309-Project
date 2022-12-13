import './style.css';
import {useState} from "react";

const buttons = [
    {title: '7', color: 'darkgrey'},
    {title: '8', color: 'darkgrey'},
    {title: '9', color: 'darkgrey'},
    {title: '/', color: 'orange'},
    {title: '4', color: 'darkgrey'},
    {title: '5', color: 'darkgrey'},
    {title: '6', color: 'darkgrey'},
    {title: '*', color: 'orange'},
    {title: '1', color: 'darkgrey'},
    {title: '2', color: 'darkgrey'},
    {title: '3', color: 'darkgrey'},
    {title: '-', color: 'orange'},
    {title: '0', color: 'darkgrey'},
    {title: '.', color: 'darkgrey'},
    {title: '=', color: 'orange'},
    {title: '+', color: 'orange'},
]

const Calculator = () => {
    const [value, setValue] = useState("");

    const click = (title) => {
        if (title === "=")
            setValue(eval(value))
        else
            setValue(value + title)
    }

    return (
        <div className="container">
            <input value={value} readOnly/>
            {buttons.map(({title, color}) => (
                <button
                    key={title}
                    onClick={() => click(title)}
                    style={{background: color}}
                >
                    {title}
                </button>
            ))}
        </div>
    )
}

export default Calculator;