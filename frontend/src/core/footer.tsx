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
  faInstagramSquare,
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
      direction="row"
      zIndex={(theme) => theme.zIndex.drawer + 1}
      bgcolor="primary.main"
      color="primary.contrastText"
      className="p-4 h-28"
    >
      <Box className = "w-1/3">
        <Typography className = "font-black text-xl">KISA</Typography>
        <Typography variant="body2"  className = "text-lg">{kisa_text}</Typography>
      </Box>
      <Box className = "w-1/3">
        <Typography className = "font-black text-xl">Contact Us</Typography>
        <Typography variant = "body2" className = "text-lg">{location}</Typography>
        <Typography variant = "body2" className = "text-lg">Phone : {phnum_kor}</Typography>
        <Typography variant = "body2" className = "text-lg">Phone : {phnum_eng}</Typography>
      </Box>
      <Box>
        <Typography className="font-black text-xl">Follow Us</Typography>
        <Stack direction="row">
          <IconButton component={Link} to="instagram.com">
            <FontAwesomeIcon icon={faInstagramSquare} size="2x"/>
          </IconButton>
          <IconButton component={Link} to="facebook.com">
            <FontAwesomeIcon icon={faFacebook} size="2x"/>
          </IconButton>
          <IconButton component={Link} to="youtube.com">
            <FontAwesomeIcon icon={faYoutube} size="2x"/>
          </IconButton>
        </Stack>
      </Box>
    </Stack>
  );
};



export default Footer;
