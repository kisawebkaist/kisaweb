import { createContext, useContext, useEffect, useState } from "react"
import { AuthAPI, User } from "../API/sso"

export type AuthContextT = {
    user: User;
    updateUser: () => void
};

const AuthContext = createContext<AuthContextT>(null!);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: React.PropsWithChildren) => {
    const [user, setUser] = useState<User>({
        is_authenticated: false,
        data: null,
    });

    const updateUser = () => AuthAPI.getUserInfo().then(setUser);

    useEffect(() => {
        AuthAPI.getUserInfo().then(setUser);
      }, [])

    return (
        <AuthContext.Provider value={{ user, updateUser }}>
            {children}
        </AuthContext.Provider>
    )
};

export default AuthProvider;