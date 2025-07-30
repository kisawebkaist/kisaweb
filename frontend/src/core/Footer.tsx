// import FacebookIcon from '@mui/icons-material/Facebook'
// import InstagramIcon from '@mui/icons-material/Instagram';
// import YouTubeIcon from '@mui/icons-material/YouTube';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "../components/css/footer.css";
import { FooterT } from "./types";
import { Box, IconButton, Typography, Stack, useTheme, Paper } from "@mui/material";
import { Link } from "react-router-dom";
import {
  faFacebook,
  faInstagram,
  faYoutube,
} from "@fortawesome/free-brands-svg-icons";
import ShapeShifter from "../components/common/ShapeShifter";

export type FooterP = {
  data: FooterT;
};

const Footer = ({
  data: {
    location,
    phnum_eng,
    phnum_kor,
    fb_link,
    insta_link,
    yt_link,
  }
}: FooterP) => {

  return (
    <Paper
      component="footer"
      sx={{
        display: "flex", 
        justifyContent: "space-between", 
        padding: 4, 
        borderRadius: 0
      }}
    >
      <ShapeShifter breakpoint="sm" down={<></>} up={
        <Stack>
          <Typography fontWeight="bold">KISA</Typography>
          <Typography variant="subtitle2">
            We are KISA.
          </Typography>
        </Stack>
      } />
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
    </Paper>
  );
};



export default Footer;
