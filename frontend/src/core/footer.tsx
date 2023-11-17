import { FooterT } from "../API/misc"
import "./footer.css"

export type FooterP = FooterT
const Footer = ({
  kisa_text, location, phnum_eng, phnum_kor, fb_link, insta_link, yt_link
}: FooterP) => {
  return (
    <footer>
      <FooterComponent topicName="KISA" description={[kisa_text]} />
      <FooterComponent topicName="Contact Us" description={[location, phnum_eng, phnum_kor]} />
      <FooterComponent topicName="Follow Us" description={[fb_link, insta_link, yt_link]} />
    </footer>
  )
}

interface FooterProps {
  topicName: string;
  description: string[];
}

function FooterComponent({ topicName, description }: FooterProps) {
  return (
    <div className="footerContainer">
      <span className="footerTopic">{topicName}</span>
      {description.map((item, index) => (
        <div key={index} className="footerElement">
          {(
            item.startsWith("http") || item.startsWith("https") ? (
              (item.includes("instagram.com")) ? (
                <a href={item} className="footerText">
                  <img src="/instagram-logo.png" className="icon" />
                </a>
              ) : (item.includes("facebook.com")) ? (
                <a href={item} className="footerText">
                  <img src="/facebook-logo.png" className="icon" />
                </a>
              ) : (item.includes("youtube.com")) ? (
                <a href={item}>
                  <img src="/youtube-logo.png" className="icon" />
                </a>
              ) : (
                <span className="footerText">{item}</span>
              )
            ) : (
              <span className="footerText">{item}</span>
            )
          )}
        </div>
      ))}
    </div>
  );
}

export default Footer
