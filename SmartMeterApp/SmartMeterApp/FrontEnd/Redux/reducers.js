import {SET_USER_PASSWORD, SET_USER_NAME} from './actions';

const initialState = {
    name: '',
    password: 0,

}

function userReducer(state = initialState, action) {
    switch (action.type) {
        case SET_USER_NAME:
            return {...state, name: action.payload};
        case SET_USER_PASSWORD:
            return {...state, password: action.payload};
        default:
            return state;
    }
}

export default userReducer;