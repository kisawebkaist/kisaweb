import { CardContent, Typography } from "@mui/material";

const personalInfoUsageStatementLastModified = "2024-06-29";
const personalInfoUsageStatement =
(
    <CardContent>
        <Typography>
            This Personal Information Usage Disclosure statement outlines how this website collects, uses, discloses and protects the personal information you provide when using our website.
        </Typography>
        <Typography>
            We may collect the following types of personal information when you use our website:
            <ul>
                <li>Demographic information (name, gender, nationality) </li>
                <li>Contact information (email) </li>
                <li>Information related to KAIST (job position, id) </li>
            </ul>
        </Typography>
        <Typography>
            We use the personal information we collect for the following purposes:
            <ul>
                <li>To provide and improve our services</li>
                <li>To personalize your experience on our website</li>
            </ul>
        </Typography>
        <Typography>
            We do not share your personal information with third parties except when required by law or to protect our rights.
            We do not sell, trade, or transfer your personal information to outside parties without your consent, except as described in this statement.
        </Typography>
        <Typography>
            We implement a variety of security measures to maintain the safety of your personal information when you enter, submit, or access your information.
        </Typography>
        <Typography>
            By using our website, you consent to our collection, use, and disclosure of your personal information as described in this statement.
        </Typography>
    </CardContent>
);

export const personalInfoUsage = {
    lastModified: personalInfoUsageStatementLastModified,
    statement: personalInfoUsageStatement,
};
