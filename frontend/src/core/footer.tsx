// import FacebookIcon from '@mui/icons-material/Facebook'
// import InstagramIcon from '@mui/icons-material/Instagram';
// import YouTubeIcon from '@mui/icons-material/YouTube';

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "../components/css/footer.css";
import { FooterT } from "./types";
import { Box, IconButton, Typography, Stack } from "@mui/material";
import { Link } from "react-router-dom";
import {
  faFacebook,
  faInstagram,
  faYoutube,
} from "@fortawesome/free-brands-svg-icons";

interface FooterProps {
  topicName: string;
  description: string[];
}

export type FooterP = {
  data: FooterT;
  compactMode: boolean;
};

const Footer = ({
  data: {
    kisa_text,
    location,
    phnum_eng,
    phnum_kor,
    fb_link,
    insta_link,
    yt_link,
  },
  compactMode,
}: FooterP) => {
  return (
    <Stack
      component="footer"
      color="text.primary"
      direction = "row"
      justifyContent="space-between"
      zIndex = {(theme) => theme.zIndex.drawer + 1}
      bgcolor = "background.default"
      className = "p-4"
    >
      {compactMode ? null : (
        <FooterComponent topicName="KISA" description={[kisa_text]} />
      )}
      <FooterComponent
        topicName="Contact Us"
        description={[location, phnum_eng, phnum_kor]}
      />
      <FooterContactComponent
        topicName="Follow Us"
        description={[fb_link, insta_link, yt_link]}
      />
    </Stack>
  );
};

function FooterContactComponent({ topicName, description }: FooterProps) {
  return (
    <Box>
      <Typography>{topicName}</Typography>
      <Stack direction="row">
        {description.map((item, index) =>
          item.includes("instagram.com") ? (
            <IconButton component={Link} to={item}>
              <FontAwesomeIcon icon={faInstagram} />
            </IconButton>
          ) : item.includes("facebook.com") ? (
            <IconButton component={Link} to={item}>
              <FontAwesomeIcon icon={faFacebook} />
            </IconButton>
          ) : (
            <IconButton component={Link} to={item}>
              <FontAwesomeIcon icon={faYoutube} />
            </IconButton>
          )
        )}
      </Stack>
    </Box>
  );
}

function FooterComponent({ topicName, description }: FooterProps) {
  return (
    <Box>
      <Typography>{topicName}</Typography>
      {description.map((item, index) => (
        <Typography variant="body2">{item}</Typography>
      ))}
    </Box>
  );
}

export default Footer;
