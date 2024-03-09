import Lister from "../components/lister";
import React, { useState } from "react";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import "../components/css/alumni.css"

/**
 * @brief This can be used as a structure of alumni api data.
 * I think we may add head of each division on top of presidents too
 */
export type AlumniDataT = {
    name: string;
    headYear: string;
    workPeriod: string;
    picture: string; //Should be great if we have
};

const fakePresidentData: AlumniDataT[] = [
    {
        name: "Ysa Margarita F. San Juan",
        headYear: "2022",
        workPeriod: "Fall 2020 - Fall 2022",
        picture: "https://qph.cf2.quoracdn.net/main-qimg-e9be1cf0430dfd81717b5450e7734d17-pjlq"
    } ,
    {
        name: "Ilham",
        headYear: "2023",
        workPeriod: "Fall 2023 - Spring2024",
        picture: "https://qph.cf2.quoracdn.net/main-qimg-e9be1cf0430dfd81717b5450e7734d17-pjlq"
    }
]

const fakeDivisionData: AlumniDataT[] = [
    {
        name: "Rick Asley",
        headYear: "2022",
        workPeriod: "Fall 2020 - Fall 2022",
        picture: "https://qph.cf2.quoracdn.net/main-qimg-e9be1cf0430dfd81717b5450e7734d17-pjlq"
    } ,
    {
        name: "John Cena",
        headYear: "2023",
        workPeriod: "Fall 2023 - Spring2024",
        picture: "https://qph.cf2.quoracdn.net/main-qimg-e9be1cf0430dfd81717b5450e7734d17-pjlq"
    }
]

//const allDivision = ["President", "Welfare Division", "Events Division", "Promotions And Public Relations Division", "Web Division", "Finance Division"]

const cardComponent = ({ data }: { data: AlumniDataT }) => {
    const [hover, setHover] = useState(false);

    const cardStyle = {
        boxShadow: hover
            ? 'rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px'
            : '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
        transform: hover ? 'scale(1.05)' : 'scale(1)'
    };
    return (
    <Card className="card" style={cardStyle}
        onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
        >
            <CardContent className="cardContent">
                <span className="date">{data.workPeriod}</span>
                <img src={data.picture} />
                <span className="headline">{data.name}</span>
                <span className="tag">{data.headYear}</span>
            </CardContent>
        </Card>
    );
}

const DivisionRender = ({ data, division }: { data: AlumniDataT[], division: string }) => {
    return (
        <>
        <center>
            <span className = "divisionName">{division}</span>
        </center>
        <div className ="cardContainer">
            <Lister
                array = {data}
                render={cardComponent}
                props={{}}
            />
        </div>
        </>
    );
}



const Alumni = () => {
    return (
        <>
        <br />
        <DivisionRender data = {fakePresidentData} division = "President" />
        <DivisionRender data = {fakeDivisionData} division = "Welfare Division" />
        <DivisionRender data = {fakeDivisionData} division = "Events Division" />
        <DivisionRender data = {fakeDivisionData} division = "Promotions And Public Relations Division" />
        <DivisionRender data = {fakeDivisionData} division = "Web Division" />
        <DivisionRender data = {fakeDivisionData} division = "Finance Division" />
        </>
    )
}

export default Alumni