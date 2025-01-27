# TTC Dashboard
From a Hack Club YSWS where you get an adafruit matrix display, thx Hack Club!

![image](https://github.com/user-attachments/assets/715c5ca0-64ad-45b9-978a-43b55f2a1b71)

- The white is the time, alternating every 5 seconds showing fullness (1-3, as on the TTC's site) and time until arrival
  - Note the API randomly returns `D` for delayed, which is odd to me cause why not just estimate a new time? oh well
- the first yellow is the current time in EST (since Toronto is in EST I left this hardcoded)
- the second yellow is the countdown until the code fetches new data, defaulted to every 30sec
  
## Usage
### TTC
You only need to supply one thing, a URL from the TTC's undocumented API :scheming-yellow-emoji: lol

Simply get your route number and stop number and format your URL as so:
```
https://www.ttc.ca/ttcapi/routedetail/GetNextBuses?routeId=[ROUTE NUMBER]&stopCode=[STOP NUMBER]
```

For example, with this stop (example, I don't live there nice try) `https://www.ttc.ca/routes-and-schedules/133/0/1375`
![image](https://github.com/user-attachments/assets/e5b83dd9-4cf3-4d4b-abf9-1ceb4eb3e194)

*Find the stop Number as highlighted and the Route Number is in red

the route is 133 and the stop number is 1375 so my URL would be:

```
https://www.ttc.ca/ttcapi/routedetail/GetNextBuses?routeId=133&stopCode=1375
```

You should also change up the user agent and stuff to avoid rate limits and stuff from other ppl (not that this project would have many users :sob:) lol

### Other Transit Agencies
This project doesn't support other agencies, but it should be simple to set up yourself! Simply find an API for your transit agency and connect the pipes :D. You'll mainly need to edit the end of the file inside the forever loop. Change the code to fetch data using whatever works for you. You'll also likely need to change up the inner loop to alternate text.
