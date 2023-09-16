import NavEntryT from "../core/navbar-type";

class NavbarAPI{
  static query = () : Promise<NavEntryT[]> => {
    // Perform the query for the navigation bar here
    // Refer to docs for details
    return new Promise<NavEntryT[]>((res, rej) => res([]))
  }
}

class MetaDatabase{
  static query = (keyName : string) : Promise<any> => {
    return new Promise<any>((res, rej) => res("lol"))
  }
}
