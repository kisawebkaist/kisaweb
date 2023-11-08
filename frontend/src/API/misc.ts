import NavEntryT from "../core/navbar-type";

class NavbarAPI {
  static query = (): Promise<NavEntryT[]> => {
    // Generate fake data for NavEntryT objects
    const fakeNavEntries: NavEntryT[] = [
      {
        type: "link",
        data: {
          href: "/home",
          text: "Home",
          style: {
            hover: { color: "blue" },
            normal: { color: "black" },
            active: { color: "red" },
          },
        },
      },
      {
        type: "link",
        data: {
          href: "/about",
          text: "About Us",
          style: {
            hover: { color: "blue" },
            normal: { color: "black" },
            active: { color: "red" },
          },
        },
      },
      // Add more fake NavEntryT objects as needed
    ];

    return Promise.resolve(fakeNavEntries);
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

class FooterAPI {
  static footer = (): Promise<FooterT> => {
    // fake footer data for development
    const fakeFooterEntries: FooterT =
      {
        kisa_text: "Kisa",
        location: "KisaRoom",
        phnum_eng: "123-456-7890",
        phnum_kor: "987-654-3210",
        email: "kisakisa@kisa.com",
        fb_link: "https://facebook.com/kisa",
        insta_link: "https://instagram.com/kisa",
        yt_link: "https://youtube.com/kisa",
      };
      
    return Promise.resolve(fakeFooterEntries);
  }
}

class MetaDatabase{
  static query = (keyName : string) : Promise<any> => {
    return new Promise<any>((res, rej) => res("lol"))
  }
}