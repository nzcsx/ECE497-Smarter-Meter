export const SET_USER_NAME = 'SET_USER_NAME';
export const SET_USER_PASSWORD = 'SET_USER_PASSWORD';

export const setName = name => dispatch => {
    dispatch({
        type: SET_USER_NAME,
        payload: name,
    });
};

export const setPassword = password => dispatch => {
    dispatch({
        type: SET_USER_PASSWORD,
        payload: password,
    });
};