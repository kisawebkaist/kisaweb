import React from "react";
import { Chart } from "../components/about-us/Chart";
import AboutUsAPI, {
  DivisionT,
  InternalBoardMemberT,
  MemberT,
} from "../API/about-us";
import QueryGuard from "../components/query-guard";
import QueryFallback from "../components/QueryFallback";
import { Box, Button, Typography } from "@mui/material";
import { Link } from "react-router-dom";

interface AboutUsP {
  divisions: DivisionT[];
  members: MemberT[];
  internalBoardMembers: InternalBoardMemberT[];
}

const AboutUs = (props: AboutUsP) => {
  return (
    <>
      {/* Hero */}
      <Box py={3} px={5}>
        <Typography variant="h3" textAlign="center">
          About Us
        </Typography>
        <Typography variant="h4" textAlign="center" py={2}>
          We are KISA, the KAIST International Students Association.
        </Typography>
        <Typography
          variant="h5"
          textAlign="center"
          color="#236FA1"
          fontWeight="bold"
        >
          Our mission is to serve the international community's interests and
          needs.
        </Typography>
        <Typography variant="body1" textAlign="justify">
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
        <Typography variant="body1" textAlign="justify">
          KISA currently has 5 divisions: Events, Welfare, Promotions and Public
          Relations, Finance, and Web. To learn more about KISA's divisions and
          what they do, you can check out the next page!
        </Typography>
      </Box>
      {/* Link to constitution */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          p: 2,
        }}
      >
        <Link to="/about-us/constitution">
          <Button
            variant="contained"
            sx={{ p: 2, fontSize: 16, fontWeight: "bold" }}
          >
            KISA Constitution &#129149;
          </Button>
        </Link>
      </Box>
      {/* Organizational chart */}
      <Box px={5}>
        {/* <Typography variant="h4" textAlign="center">
          KAIST International Students Association
        </Typography> */}
        <Typography variant="h3" textAlign="center" fontWeight="bold">
          Organizational Chart
        </Typography>
        {/* Chart */}
        <Chart
          divisions={props.divisions}
          members={props.members}
          internalBoardMembers={props.internalBoardMembers}
        />
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
