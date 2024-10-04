 import axios from "axios";

export default class MiscAPI {
  static query = <T> (path: string,fallback: () => T): Promise<T> => axios.get(`${process.env.REACT_APP_API_ENDPOINT}/misc/${path}`).then((res)=>res.data, fallback);
}

class MetaDatabase{
  static query = (keyName : string) : Promise<any> => {
    return new Promise<any>((res, rej) => res("lol"))
  }
}
