```mermaid
flowchart TD

A[Start] --> B[Load user input]
B --> C[Load POI Dataset]
C --> D{POI open?}
D -- No --> C
D -- Yes --> E[Compute distance]
E --> F[Compute travel time]
F --> G{Time fits user's end_time?}
G -- No --> C
G -- Yes --> H[Compute score]
H --> C
C --> I[Sort by score desc]
I --> J[Pick top K]
J --> K[Return suggestions]
K --> L[End]
