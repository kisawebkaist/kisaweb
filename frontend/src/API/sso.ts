import axios from "axios";
import { User } from "../core/types";

export class AuthAPI {
    static login = (next: string): Promise<string> => axios.post(`${process.env.REACT_APP_API_ENDPOINT}/sso/login/`, {next: next}).then(r => r.data['redirect']);
    static logout = (next: string): Promise<string> => axios.post(`${process.env.REACT_APP_API_ENDPOINT}/sso/logout/`, {next: next}).then(r => r.data['redirect']);
    static userinfo = (): Promise<User> => axios.get(`${process.env.REACT_APP_API_ENDPOINT}/sso/userinfo/`).then(r => r.data);
}