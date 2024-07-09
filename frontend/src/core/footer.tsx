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

export type FooterP = {
  data: FooterT;
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
  }
}: FooterP) => {
  return (
    <Stack
      component="footer"
      direction="row"
      zIndex={(theme) => theme.zIndex.drawer + 1}
      bgcolor="primary.main"
      color="primary.contrastText"
      className="p-4"
      sx={{display: "flex", justifyContent: "space-between"}}
    >
      <Box sx={{ display: {xs: 'none', sm: 'none', md: 'block'} }}>
        <Typography fontWeight="bold">KISA</Typography>
        <Typography variant="subtitle2">
          {kisa_text}
        </Typography>
      </Box>
      <Box>
        <Typography fontWeight="bold">Contact Us</Typography>
        <Typography variant="subtitle2">
          {location}<br/>
          Phone: {phnum_kor}<br/>
          Phone: {phnum_eng}
        </Typography>
      </Box>
      <Box>
        <Typography fontWeight="bold">Follow Us</Typography>
        <Stack direction="row">
          <IconButton component={Link} to={insta_link}>
            <FontAwesomeIcon icon={faInstagram}/>
          </IconButton>
          <IconButton component={Link} to={fb_link}>
            <FontAwesomeIcon icon={faFacebook}/>
          </IconButton>
          <IconButton component={Link} to={yt_link}>
            <FontAwesomeIcon icon={faYoutube}/>
          </IconButton>
        </Stack>
      </Box>
    </Stack>
  );
};



export default Footer;
