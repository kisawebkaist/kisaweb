import { createContext } from "react"
import { User } from "../API/sso"

export type AppContextT = {
    user: User
    dispatch: AppContextDispatcher;
}

export interface AppContextActionCallback<In> {
    data: In,
    dispatch(prev: AppContextT): AppContextT;
}

export class UserUpdate implements AppContextActionCallback<User>{
    data: User;

    constructor(data: User) {
        this.data = data;
    }

    dispatch(prev: AppContextT): AppContextT {
        prev.user = this.data;
        return prev;
    }
}

export class DispatcherUpdate implements AppContextActionCallback<AppContextDispatcher> {
    data: AppContextDispatcher;

    constructor(data: AppContextDispatcher) {
        this.data = data;
    }

    dispatch(prev: AppContextT): AppContextT {
        prev.dispatch = this.data;
        return prev;
    }
}

export class NoOp implements AppContextActionCallback<{}> {
    data = {};

    dispatch(prev: AppContextT): AppContextT {
        return prev;
    }
}

export type AppContextAction = NoOp|UserUpdate|DispatcherUpdate;
export type AppContextDispatcher = (action: AppContextAction) => void;

export function appContextReducer(state: AppContextT, action: AppContextAction) {
    action.dispatch(state)
}

export const defaultAppContext: AppContextT = {
    user: {
        is_authenticated: false,
        data: null
    },
    dispatch: (action) => {}
};

/**
 * The context for the whole application.
 * 
 */
export const AppContext = createContext<AppContextT>(defaultAppContext);

export default AppContext;
