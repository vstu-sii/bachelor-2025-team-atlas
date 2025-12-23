export default function RootLayout({ children }) {
    return (
        <html>
            <head>
                <title>My Frontend</title>
            </head>
            <body>{children}</body>
        </html>
    );
}