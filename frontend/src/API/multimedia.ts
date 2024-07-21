import axios from "axios";

export type MultimediaT = {
    title: string;
    description: string;
    images: MultimediaImageT[];
    slug: string;
};

export type MultimediaImageT = {
    alt: string;
    href: string;
    date: string;
};


export const fakeMultimediaData: MultimediaT[] = [
    {
        title: "2023 Spring OT",
        description: "Never gonna give you up",
        images: [
            {
                alt: "Lorem ipsum",
                href: "https://images.unsplash.com/photo-1607827447604-d9a8c439186e?fm=jpg&w=3000&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09541.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09659_1.jpg",
                date: "Sat, 15 Jul 2024 06:34:08 GMT",
            }
        ],
        slug: "23Spring"
    },
    {
        title: "2024 Spring OT",
        description: "Never gonna let you down",
        images: [
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09569.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09569.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09569.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            }
        ],
        slug: "24Spring"
    },
    {
        title: "2025 Spring OT",
        description: "Never gonna run around and desert you",
        images: [
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09541.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09541.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            },
            {
                alt: "Lorem ipsum",
                href: "https://kisa.kaist.ac.kr/media/images/BAR09541.jpg",
                date: "Sat, 13 Jul 2024 06:34:08 GMT",
            }
        ],
        slug: "25Spring"
    }
];

export default class MultimediaAPI {
    static all = () => axios
        .get(`/api/multimedia/`)
        .then(resp => resp.data as MultimediaT[])
}