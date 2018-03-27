package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/mmcdole/gofeed"
)

func handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"+
		"<title>%s</title></head><body>", r.URL.Path[1:])
	fmt.Fprintf(w, "<pre>")
	fmt.Fprintf(w, "--- Hot topics ---\n")
	fmt.Fprintf(w, "<a href=\"https://www.cisecurity.org/cybersecurity-threats/\">cibersecurity-threats</a>\n")
	fmt.Fprintf(w, "\n")
	fmt.Fprintf(w, "Hi there, I love %s!\n", r.URL.Path[1:])
	fmt.Fprintf(w, "Yeah, %s!\n", r.URL.Path[1:])
	fmt.Fprintf(w, "--- See below useful results for: %s ---\n", r.URL.Path[1:])

	fp := gofeed.NewParser()
	feed, _ := fp.ParseURL("http://feeds.twit.tv/twit.xml")
	//	fmt.Println(feed.Title)
	fmt.Fprintf(w, "\n")
	fmt.Fprintf(w, "<a href=%s>%s</a>", feed.Link, feed.Title)
	fmt.Fprintf(w, "\n")
	fmt.Fprintf(w, "\n")
	fmt.Fprintf(w, "%+v\n", feed)
	fmt.Fprintf(w, "</pre>")
	fmt.Fprintf(w, "</body></html>")
	fmt.Fprintf(w, "\n")

}

func main() {
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
