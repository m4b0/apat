package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"

	"github.com/mmcdole/gofeed"
)

func handler(w http.ResponseWriter, r *http.Request) {
	// HTML Header
	fmt.Fprintf(w, "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"+
		"<title>apat %s</title></head><body>", r.URL.Path[1:])
	fmt.Fprintf(w, "<pre>")

	// Title
	fmt.Fprintf(w, "<b><a href=\"https://github.com/m4b0/apat\">apat</a> (a path) - another personalized aggregator tool</b>\n")
	fmt.Fprintf(w, "\n")

	// Hot Topics
	fmt.Fprintf(w, "<b>--- Hot topics ---</b>\n")
	fmt.Fprintf(w, "\n")
	path := "sources/hot-topics.src"
	inFile, _ := os.Open(path)
	scanner := bufio.NewScanner(inFile)
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		content := strings.Split(scanner.Text(), " - ")
		url := content[0]
		resp, err := http.Get(url)

		if err != nil {
			fmt.Println("ERROR: Failed to crawl \"" + url + "\"")
			return
		}

		bodyBytes, err := ioutil.ReadAll(resp.Body)
		bodyString := string(bodyBytes)

		lookFor := content[3]
		//fmt.Fprintf(w, "<textarea>%+v</textarea>\n", lookFor)
		re := regexp.MustCompile(lookFor)
		matches := re.FindStringSubmatch(bodyString)
		if len(matches) > 0 {
			fmt.Fprintf(w, "<a href=\"%s\">%s</a> %s %q\n", content[0], content[1], content[2], matches[1])
		} else {
			fmt.Fprintf(w, "<a href=\"%s\">%s</a> %s Not-Found\n", content[0], content[1], content[2])
		}

		resp.Body.Close() // close Body when the function returns
	}
	fmt.Fprintf(w, "\n")
	inFile.Close()

	// Topics
	files, err := ioutil.ReadDir("./topics")
	if err != nil {
		log.Fatal(err)
	}

	for _, f := range files {
		fmt.Fprintf(w, "<b>--- %s ---</b>\n", f.Name())

		path := "sources/" + f.Name() + ".src"
		inFile, _ := os.Open(path)
		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		for scanner.Scan() {
			feedUrl := scanner.Text()

			fp := gofeed.NewParser()
			//feed, _ := fp.ParseURL("http://feeds.twit.tv/twit.xml")
			feed, _ := fp.ParseURL(feedUrl)
			fmt.Fprintf(w, "\n")
			if len(feed.Title) > 1 {
				fmt.Fprintf(w, "<b><a href=\"%s\">%s</a></b>", feed.Link, feed.Title)
			} else {
				fmt.Fprintf(w, "<b><a href=\"%s\">%s</a></b>", feed.Link, feed.Link)
				//fmt.Fprintf(w, "%+v\n", feed)
			}
			fmt.Fprintf(w, "\n")
			fmt.Fprintf(w, " - <a href=\"%s\">%s</a> (%s)", feed.Items[0].Link, feed.Items[0].Title, feed.Items[0].Published)
			fmt.Fprintf(w, "\n")
			fmt.Fprintf(w, " - <a href=\"%s\">%s</a> (%s)", feed.Items[1].Link, feed.Items[1].Title, feed.Items[1].Published)
			fmt.Fprintf(w, "\n")
			fmt.Fprintf(w, " - <a href=\"%s\">%s</a> (%s)", feed.Items[2].Link, feed.Items[2].Title, feed.Items[2].Published)
			fmt.Fprintf(w, "\n")
			fmt.Fprintf(w, "\n")
			//		fmt.Fprintf(w, "%+v\n", feed)
		}

		inFile.Close()
	}
	// Footer
	fmt.Fprintf(w, "</pre>")
	fmt.Fprintf(w, "</body></html>")
	fmt.Fprintf(w, "\n")

}

func main() {
	http.HandleFunc("/", handler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
