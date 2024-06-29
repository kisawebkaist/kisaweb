import FacebookIcon from '@mui/icons-material/Facebook'
import InstagramIcon from '@mui/icons-material/Instagram';
import YouTubeIcon from '@mui/icons-material/YouTube';

import "../components/css/footer.css"
import { FooterT } from "./types";
import { Box, IconButton, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

interface FooterProps {
  topicName: string;
  description: string[];
}

export type FooterP = {
  data: FooterT;
  compactMode: boolean;
}

const Footer = ({ data: {
  kisa_text, location, phnum_eng, phnum_kor, fb_link, insta_link, yt_link
}, compactMode }: FooterP) => {
  return (
    <Box component='footer' color='text.primary' sx={{ width: '100%', bgcolor: 'background.default', display: 'flex', flexDirection: 'row', justifyContent: 'space-around', zIndex: (theme) => theme.zIndex.drawer + 1 }} >
      {
        compactMode ? null: <FooterComponent topicName="KISA" description={[kisa_text]} />
      }
      <FooterComponent topicName="Contact Us" description={[location, phnum_eng, phnum_kor]} />
      <FooterContactComponent topicName="Follow Us" description={[fb_link, insta_link, yt_link]} />
    </Box>
  )
}

function FooterContactComponent({ topicName, description }: FooterProps) {
  return (
    <Box>
      <Typography>{topicName}</Typography>
      <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'center'}}>
        {
          description.map((item, index) => 
            item.includes("instagram.com") ? (
              <IconButton component={Link} to={item}>
                <InstagramIcon/>
              </IconButton>
            ) : item.includes("facebook.com") ? (
              <IconButton component={Link} to={item}>
                <FacebookIcon/>
              </IconButton>
            ) : (
              <IconButton component={Link} to={item}>
                <YouTubeIcon/>
              </IconButton>
            )
          )
        }
      </Box>
    </Box>
  );
}



function FooterComponent({ topicName, description }: FooterProps) {
  return (
    <Box>
      <Typography>{topicName}</Typography>
      {
        description.map((item, index) => <Typography variant='body2'>{item}</Typography>)
      }
    </Box>
  );
}

export default Footer
