export type FooterP = {
  kisa_text : string
  location : string
  phnum_eng : string
  phnum_kor : string
  email : string
  fb_link : string
  insta_link : string
  yt_link : string
}

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
