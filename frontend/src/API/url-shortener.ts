import axios from "axios";

export default class UrlShortener {
  static expandUrl(name: string): Promise<string> {
    return axios
      .get(`${process.env.REACT_APP_API_ENDPOINT}short-link/${name}`)
      .then((resp) => resp.data);
  }
}
