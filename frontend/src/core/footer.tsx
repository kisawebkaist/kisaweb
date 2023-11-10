import { FooterT } from "../API/misc"

export type FooterP = FooterT
const Footer = ({
  kisa_text, location, phnum_eng, phnum_kor, fb_link, insta_link, yt_link
} : FooterP) => {
  return (
    <footer>
      <FooterComponent topicName="KISA" description = { [kisa_text] } />
      <FooterComponent topicName="Contact Us" description = {[location, phnum_eng, phnum_kor ]} />
      <FooterComponent topicName="Follow Us" description = {[fb_link, insta_link, yt_link] } />
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
      <div>
        {description.map((item, index) => (
          <div key={index}>
            {(
              item.startsWith("http") || item.startsWith("https") ? (
                //maybe we should have new properties like alias of the link
                <a href={ item } className="footerText">
                  { item }
                </a>
              ) : (
                <span className = "footerText">{ item }</span>
              )
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Footer
