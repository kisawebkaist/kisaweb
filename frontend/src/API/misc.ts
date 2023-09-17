import NavEntryT from "../core/navbar-type";

class NavbarAPI{
  static query = () : Promise<NavEntryT[]> => {
    // Perform the query for the navigation bar here
    // Refer to docs for details
    return new Promise<NavEntryT[]>((res, rej) => res([]))
    /**
     * @example
     * return axios.get(someUrl).then()
     */
  }
}

export type FooterT  = {
  kisa_text : string
  location : string
  phnum_eng : string
  phnum_kor : string
  email : string
  fb_link : string
  insta_link : string
  yt_link : string
}

class FooterAPI{
  static footer = () : Promise<FooterT> => {

  }
}

class MetaDatabase{
  static query = (keyName : string) : Promise<any> => {
    return new Promise<any>((res, rej) => res("lol"))
  }
}
