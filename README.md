# Fundamentals of Software Systems (HS21): Task 1

## Discussion Points

> Which serialization algorithm performs better, and why? Algorithms may perform
differently based on the type of data at hand (i.e., structured, semi-structured,
unstructured). In this sense, developers need to identify what types of data the
application handles to determine which algorithm is most suitable.

The application receives unstructured data as input and serializes it using JSON and Pickle 
serialization algorithms.
For our experiments and benchmarks, Pickle serialization was much faster than JSON algorithm, with this discrepancy being more noticeable for larger files.  Since the application is powered by Python, it is expected that Pickle would be the faster serialization algorithm. Pickle is highly optimized for Python processes (and is Python-specific). Most noteable, it keeps track of objects it has already serialized, such that later references to the same object won’t be serialized again. Given the fact that we were asked to do multiple runs, this optimization makes Pickle the favorable serialization algorithm for this task. Also, while JSON serializes text and must convert data to a human-readable format, Pickle uses a compact binary representation and must not necessarily output human-readable data, which 
are yet other performance gains.

> Aligned to the previous discussion point, what is the impact on file size (in percentage
terms) for the test files? Is it possible to conclude that serialization is
particularly advantageous for relatively large files (e.g., 1 Gb)?

The impact of file size is very different depending on the serialization algorithm. However, 
for both algorithms there was a significant increase in the overall duration of the serialization 
process for larger files. For JSON the file size had a larger impact compared to Pickle. This may be explained by the abovementionned performance optimizations.

*TODO: Add some numbers when we have our plots.*

I wouldn't say that serialization is better for larger files, because its file size after serialization may explore (depending on the algorithm), the larger the initial file size. Therefore, serialization is better used for smaller payloads.

> At what point (if any) does the decentralized storage perform better than centralized?
As previously mentioned (cf. Section 2), depending on factors such as
the size of the file to be stored and the performance (involving several factors) of
the server, the centralized approach can be more advantageous. For example,
for relatively small files (e.g., 1 Mb), the use of a decentralized server may represent
an unnecessary overhead, but for relatively large files (e.g., 1 Gb), there
may be significant performance gains in file retrieval.

For large files, a decentralized server can be advantageous, because we can get parts of the
content from many different peers, which may be geographically closer to us than a centralized server. It also allows to 
download files in parallel compared to a centralized access, which improves the time to download files. Additionally, a centralized server may also be a bottleneck/ single point-of-failure when retrieving large files which usually take quite some time. In contrast, decentralized file storage can still be completed if one peer fails, since we can use another peer to download the missing parts. Finally, by using a decentralized server, we reduce network loads by not directly downloading large files from one host only, but rather download small pieces from different peers.

> One of the great advantages of HTTP is its extensive documentation as it is an
”industry-standard” protocol. In this sense, how does the group evaluate the
experience using IPFS (1-10) considering aspects like available documentation
and implementation experience?

In terms of documentation, there is plenty available. The [official docs](https://docs.ipfs.io/) provide a sufficiently in-depth guide for the available installation methods. Additionally, instructions on usage, important concepts as well as links to community sites and tutorials are present.

The implementation experience is not as satisfactory when compared to the availability of information/documentation. This is mostly due to the fact that - at least in comparison to HTTP - a lot of additional steps are necessary to get set up. Plus, sometimes things were just not running smoothly, e.g., files would be inconsistent in terms of availability, sometimes not being available at all and other times having wildly varying  download speeds, which left us unclear on whether we messed up in our setup or if the technology simply has not quite matured yet.

In our eyes, it is mostly the implementation experience that drags down the score, as the documentation side of things leaves very little to be desired.

Scores:
* Documentation: 9
* Implementation Experience: 7
* Overall: 8

> Time elapsed to serialize and store (combined plot comparing two selected algorithms):

-->  insert plot

> Time elapsed to retrieve and deserialize (combined plot comparing two selected
algorithms):

--> insert plot

> Time elapsed to serialize and store a picture or image (combined plot comparing
two selected algorithms):

--> insert plot
