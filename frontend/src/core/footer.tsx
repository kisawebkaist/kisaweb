import "../components/css/footer.css"
import fakeFooterData from "./fakeDataForFooter";
import { FooterT } from "./types";

interface FooterProps {
  topicName: string;
  description: string[];
}

export class FooterP {
  data: FooterT;

  constructor(
    data: FooterT = fakeFooterData
  ) {
    this.data = data;
  }
}

const Footer = ({ data: {
  kisa_text, location, phnum_eng, phnum_kor, fb_link, insta_link, yt_link
}}: FooterP) => {
  return (
    <footer>
      <FooterComponent topicName="KISA" description={[kisa_text]} />
      <FooterComponent topicName="Contact Us" description={[location, phnum_eng, phnum_kor]} />
      <FooterContactComponent topicName="Follow Us" description={[fb_link, insta_link, yt_link]} />
    </footer>
  )
}

function FooterContactComponent({ topicName, description }: FooterProps) {
  return (
    <div className="footerContact">
      <span className="footerTopic">{topicName}</span>
      <div className="contactElement">
        {
          description.map((item, index) => (
            <div key={index} className="footerElement">
              {
                item.includes("instagram.com") ? (
                  <a href={item} className="footerText">
                    <img src="/instagram-logo.png" className="icon" alt="Instagram" />
                  </a>
                ) : item.includes("facebook.com") ? (
                  <a href={item} className="footerText">
                    <img src="/facebook-logo.png" className="icon" alt="Facebook" />
                  </a>
                ) : (
                  <a href={item} className="footerText">
                    <img src="/youtube-logo.png" className="icon" alt="YouTube" />
                  </a>
                )
              }
            </div>
          ))
        }
      </div>
    </div>
  );
}



function FooterComponent({ topicName, description }: FooterProps) {
  return (
    <div className="footerContainer">
      <span className="footerTopic">{topicName}</span>
      {description.map((item, index) => (
        <div key={index} className="footerElement">
          {
            (
              <span className="footerText">{item}</span>
          )
          }
        </div>
      ))}
    </div>
  );
}

export default Footer
