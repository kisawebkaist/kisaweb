import React from "react";
import QueryGuard from "../../components/common/QueryGuard";
import QueryFallback from "../../components/common/QueryFallback";
import { Box, Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import { HighlightedLetter } from "../../components/common/HighlightedLetter";
import AboutUsAPI, { getKISADivisionName, KISADivision, KISADivisionContent, KISAMember } from "../../API/about-us";
import { Editor } from "draft-js";
import TextEditor from "@jowillianto/draftjs-wysiwyg/dist";
import { Chart } from "./Chart";

interface AboutUsProps{
  divisions: KISADivisionContent[];
  members: KISAMember[];
}

const CONSTITUTION_LINK = "/KISAConstitution.pdf";

const AboutUs = (props: AboutUsProps) => {
  const DivisionDescription = (division: KISADivisionContent) => {
    return (
      <li>
        <Typography variant="h3">{getKISADivisionName(division.division)}</Typography>
        <TextEditor defaultValue={division.content} editorBehaviour={{readOnly: true}}/>
      </li>
    );
  }
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
            members={props.members}
          />
        </Box>
        <Typography>
          Want more detail about KISA? We got you covered. Here's our <Link to={CONSTITUTION_LINK}>constitution</Link>.
        </Typography>
        <Typography variant="h2">Divisions</Typography>
        <Typography component="div">
          As we work on different aspects to improve the life of international students in KAIST, currently, there are 5 divisions in KISA.
          <ul>
            {props.divisions.map(DivisionDescription)}
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
  const query = React.useCallback<(params: undefined) => Promise<AboutUsProps>>(
    async (params: undefined) => {
      const divisions = await AboutUsAPI.getDivisionContentList();
      const members = await AboutUsAPI.getMemberList();
      return {
        divisions,
        members,
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
