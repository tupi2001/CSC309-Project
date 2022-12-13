import React from "react";
import Text from "../Text";

class Input extends React.Component {
    render(){
        const { title, value, update } = this.props;
        return (
            <>
                <Text>{ title }</Text>
                <input
                    type="text"
                    value={value}
                    onChange={event => update(event.target.value)}
                    style={{height: 40, width: 200, fontSize: '2rem'}}
                />
            </>
        )
    }
}

export default Input;