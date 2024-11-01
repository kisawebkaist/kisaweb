import React from "react";
import { Chart } from "../../components/about-us/Chart";
import AboutUsAPI, {
  DivisionT,
  InternalBoardMemberT,
  MemberT,
} from "../../API/about-us";
import QueryGuard from "../../components/common/QueryGuard";
import QueryFallback from "../../components/common/QueryFallback";
import { Box, Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { HighlightedLetter } from "../../components/common/HighlightedLetter";

interface AboutUsP {
  divisions: DivisionT[];
  members: MemberT[];
  internalBoardMembers: InternalBoardMemberT[];
}

const constitutionLink =
  "https://www.researchgate.net/profile/Martin-Monperrus/publication/359971198_Exhaustive_Survey_of_Rickrolling_in_Academic_Literature/links/63d2405bd9fb5967c206fdf0/Exhaustive-Survey-of-Rickrolling-in-Academic-Literature.pdf?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19";

const AboutUs = (props: AboutUsP) => {
  return (
    <>
      {/* Hero */}
      <Stack py={3} px={5}>
        <Typography variant="fancy_h1" textAlign="center">
          About <HighlightedLetter letter="Us" />
        </Typography>
        <Typography textAlign="center" py={2}>
          Some quote
        </Typography>
        <Stack>
          <Typography variant="h2">What is KISA?</Typography>
          <img src="https://kisa.kaist.ac.kr/static/img/members.png" alt="KISA Members" width="100%"/>
          <Typography variant="body1" textAlign="justify">
            KISA stands for "KAIST International Student Association".
            KISA was founded in 2004, from the need to represent the voice of the
            international community to KAIST administration. Since its origin,
            KISA has been working continuously to improve the lives of the
            international students at KAIST. KISA has brought many memorable
            events and initiatives for the past 19 years such as the annual KAIST
            International Food Festival (Spring) and Sports Festival (Fall), KISA
            Scavenger Hunt, KISA Chuseok Party, KISA Halloween Party, KISA
            Lotteria Meal Scholarship, KISA Course Resources, increase in part
            time jobs availability, and many more.
          </Typography>
          <Typography variant="h2">Internal Mechanics of KISA</Typography>
          <Typography variant="body1" textAlign="justify">
            Briefly explain the role of three people in the chart.
          </Typography>
        </Stack>
        {/* Organizational chart */}
        <Box 
          px={"2vw"}
          sx={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          {/* Chart */}
          <Chart
            divisions={props.divisions}
            members={props.members}
            internalBoardMembers={props.internalBoardMembers}
          />
        </Box>
        <Typography>
        Want more detail about KISA? We got you covered. Here's our <Link to={"/"}>constitution</Link>.
        </Typography>
        <Typography variant="h2">Divisions</Typography>
        <Typography component={"div"}>
          As we work on different aspects to improve the life of international students in KAIST, currently, there are 5 divisions in KISA.
          <ul>
            <li>
              Welfare division 🫰 - 
            </li>
            <li>
              Events division 🎉 - 
            </li>
            <li>
              Promotions and Public Relations division 🎥 -
            </li>
            <li>
              Web division 🖥️ - 
            </li>
            <li>
              Finance division 💰 - 
            </li>
          </ul>
        </Typography>
      </Stack>

      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          p: 2,
        }}
      >
        {/* <Button
          variant="contained"
          sx={{ p: 2, fontSize: 16, fontWeight: "bold" }}
          href={constitutionLink}
        >
          KISA Constitution &#129149;
        </Button> */}
      </Box>
      
    </>
  );
};

const AboutUsWithGuard = () => {
  const query = React.useCallback<(params: undefined) => Promise<AboutUsP>>(
    async (params: undefined) => {
      const divisions = await AboutUsAPI.divisions();
      const members = await AboutUsAPI.members();
      const internalBoardMembers = await AboutUsAPI.internalMembers();
      return {
        divisions,
        members,
        internalBoardMembers,
      };
    },
    []
  );
  return (
    <QueryGuard
      render={AboutUs}
      props={{}}
      query={query}
      args={undefined}
      fallback={QueryFallback()}
    />
  );
};

export default AboutUsWithGuard;
