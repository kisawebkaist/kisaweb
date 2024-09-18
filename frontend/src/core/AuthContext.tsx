import { createContext, useContext } from "react"
import { User } from "../API/sso"

export type AuthContextT = {
    user: User;
    updateUser: (user: User) => void
};

export const defaultAuthContext: AuthContextT = {
    user: {
        is_authenticated: false,
        data: null
    },
    updateUser: (user: User) => {}
};

export const AuthContext = createContext<AuthContextT>(defaultAuthContext);

export const useAuth = () => useContext(AuthContext);

export default AuthContext;