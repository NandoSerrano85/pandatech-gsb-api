import {useState} from 'react';
import PropTypes from 'prop-types';

const Dropdown = (props) => {

    return (
        <></>
    )
};

Dropdown.propTypes = {
    label: PropTypes.string.isRequired,
    image: PropTypes.shape({
        path: PropTypes.string,
        alt:PropTypes.string,
    }),
};

export default Dropdown;