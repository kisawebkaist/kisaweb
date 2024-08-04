import axios from "axios";

export type UserInfo = {
    name: string;
    studentid: string;
    email: string;
  }
interface BaseUser {
is_authenticated: boolean,
data: UserInfo | null,
}
export interface AnonymousUser extends BaseUser {
is_authenticated: false,
data: null,
}
export interface AuthenticatedUser extends BaseUser {
    is_authenticated: true,
    data: UserInfo,
}
export type User = AuthenticatedUser | AnonymousUser;
export class AuthAPI {
    static login = (next: string): Promise<string> => axios.post(`${process.env.REACT_APP_API_ENDPOINT}/sso/login/`, {next: next}).then(r => r.data['redirect']);
    static logout = (next: string): Promise<string> => axios.post(`${process.env.REACT_APP_API_ENDPOINT}/sso/logout/`, {next: next}).then(r => r.data['redirect']);
    static userinfo = (): Promise<User> => axios.get(`${process.env.REACT_APP_API_ENDPOINT}/sso/userinfo/`).then(r => r.data);
}