import { Button, Card, CardActionArea, CardHeader, CardMedia, Dialog, DialogActions, DialogContent, DialogContentText, Divider, Grid, Snackbar, Stack, Typography } from "@mui/material";
import { EventAPI, EventT_Partial } from "../../API/events";
import Lister from "../../components/common/Lister";
import { useLocation, useNavigate } from "react-router-dom";
import QueryGuard from "../../components/common/QueryGuard";
import { useEffect, useRef, useState } from "react";
import TextEditor from "@jowillianto/draftjs-wysiwyg/dist";
import { useNotification } from "../../core/NotificationContext";

function getSemesterFromDate(date: Date) {
    let month = date.getMonth();
    let year = date.getFullYear().toString();
    if (month < 3)
        return year + ' Winter';
    if (month < 7)
        return year + ' Spring';
    if (month < 9)
        return year + ' Summer';
    return year + ' Fall';
}

type EventP = {
    events: EventT_Partial[];
}

export const Event = ({ events }: EventP) => {
    const location = useLocation();
    const navigate = useNavigate();
    const notification = useNotification();
    const [slug, setSlug] = useState<string>((location.hash as string).replace("#", ""));
    const dialogInner = useRef(<></>);

    const onCopyLink = () => {
        navigator.clipboard.writeText(window.location.protocol+"//"+window.location.host+location.pathname+"#"+slug);
        notification.showNotification("Link copied to clipboard!");
    }

    useEffect(() => {
        if (slug !== "") {
            EventAPI.getEvent(slug)
                .then(
                    event => {
                        dialogInner.current = (
                            <DialogContent>
                                <Stack>
                                    <Typography variant="h3" textAlign="center">
                                        {event.title}
                                    </Typography>
                                    <TextEditor
                                        defaultValue={event.description}
                                        editorBehaviour={{ readOnly: true }}
                                    />
                                </Stack>
                            </DialogContent>
                        );
                    },
                    error => {
                        console.error(error);
                        setSlug("");
                    }
                )
                .then(
                    () => navigate("#" + slug)
                )
            return;
        }
        navigate("");
    }, [navigate, slug])

    const EventCard = ({ data }: { data: EventT_Partial }) => {

        return (
            <Grid item xs={12} md={6} lg={4}>
                <Card>
                    <CardActionArea
                        onClick={() => setSlug(data.slug)}
                    >
                        <CardMedia
                            component="img"
                            alt={"Poster for " + data.title}
                            image={data.poster}
                        />
                        <CardHeader title={data.important_message} />
                    </CardActionArea>
                </Card>
            </Grid>
        )
    };

    const UpcomingEvents = ({ events }: EventP) => {
        const now = new Date();
        const toRender = events.filter(event => new Date(event.event_start_datetime) >= now);
        if (toRender.length === 0) {
            return null;
        }

        return (
            <>
                <Typography variant="h2" color="main">Upcoming Events</Typography>
                <Grid container spacing={4} className="p-4">
                    <Lister array={toRender} render={EventCard} props={undefined} />
                </Grid>
            </>
        )
    };

    const EventCardsCategorizedBySemester = ({ events }: {events: EventT_Partial[]}) => {
        let semesterArchives: JSX.Element[] = [];
        let currentSemester = getSemesterFromDate(new Date());
        let currentSemesterArchive: JSX.Element[] = [];

        function archiveCurrentSemester() {
            if (currentSemesterArchive.length !== 0) {
                semesterArchives.push(<Typography variant="h2" key={currentSemester+"-title"}>{currentSemester}</Typography>)
                semesterArchives.push(
                    <Grid container spacing={4} className="p-4" key={currentSemester}>
                        {currentSemesterArchive}
                    </Grid>
                );
                semesterArchives.push(<Divider key={currentSemester+"-divider"}/>);
            }
        }
        
        for (let event of events) {
            let semester = getSemesterFromDate(new Date(event.event_start_datetime));
            if (semester !== currentSemester) {
                archiveCurrentSemester();
                currentSemester = semester;
                currentSemesterArchive = [];
            }
            currentSemesterArchive.push(<EventCard data={event} key={event.slug}/>);
        }
        archiveCurrentSemester();
        return (
            <>
                <Typography variant="h2" textAlign="center">All events</Typography>
                <Divider />
                {semesterArchives}
            </>
        )
    }

    return (
        <Stack>
            <Dialog open={slug !== ""} onClose={() => setSlug("")}>
                {dialogInner.current}
                <DialogActions>
                    <Button onClick={() => setSlug("")}>
                        Cancel
                    </Button>
                    <Button onClick={onCopyLink}>
                        Copy Link
                    </Button>
                    <Button>
                        Register
                    </Button>
                </DialogActions>
            </Dialog>
            <Stack textAlign="center">
                <Typography variant="fancy_h1" textAlign="center">Events</Typography>
                <Typography variant="subtitle1">Lorem ipsum</Typography>
            </Stack>
            <UpcomingEvents events={events} />
            <EventCardsCategorizedBySemester events={events} />
        </Stack>
    )
};

const EventWithGuard = () => {
    const query = (args: Record<string, any>) => EventAPI.allEvents(args).then((events) => {
        return {
            events: events
        }
    })
    return (
        <QueryGuard
            query={query}
            args={{}}
            render={Event}
            props={{}}
        />
    )
}

export default EventWithGuard;