# foot

Web Crawling Project

Foot is a library that fetches a list of URLs and silly walks through each site to gather information.

## Usage
### Install   

`pip install foot`  

#### foot (cli)

- `-u` URL(s) (encapsulated in quotes, separated by commas) 
- `-f` filename (list of urls on new lines)

##### Options (not required)

- `-c` : Specify chunk size (default=10)
- `--recursive` : Enable one level of recursion 

##### Examples:

Array of URLS:  
`foot -u 'http://example.com, http://example1.com'`  

Array of URLS with Options:  
`foot 'http://example.com, http://example1.com' -c 5 --recursive`  

File:  
`foot -f 'example.txt`

File with Options:  
`foot -f 'example.txt' -c 5 --recursive`   

## Module

Import:  
`import foot`  


### Functions

The `get` function takes an array of URLS and options. 

```javascript
foot.get(["http://www.example`.com", "http://www.example2.com"], options);
    => Data output in ./foot/url.json and foot-date.txt
```

The `file` function takes a filename and options. 

```python
foot.file("./test.txt", recursive=True)
    => Data output in ./foot/url.json and foot-date.txt
```