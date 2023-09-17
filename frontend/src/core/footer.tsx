import { FooterT } from "../API/misc"

export type FooterP = FooterT
const Footer = ({
  kisa_text, location, phnum_eng, phnum_kor, fb_link, insta_link, yt_link
} : FooterP) => {
  return (
    <footer>
      <h1> Hello Footer </h1>
    </footer>
  )
}

export default Footer
