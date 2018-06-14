package test2

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class RecordedSimulation extends Simulation {

	val httpProtocol = http
		.baseURL("http://detectportal.firefox.com")
		.inferHtmlResources()
		.userAgentHeader("Microsoft-WNS/6.3")

	val headers_0 = Map(
		"Accept" -> "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Encoding" -> "gzip, deflate",
		"Accept-Language" -> "en-US,en;q=0.5",
		"Connection" -> "keep-alive",
		"Upgrade-Insecure-Requests" -> "1",
		"User-Agent" -> "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0")

	val headers_1 = Map(
		"Accept" -> "*/*",
		"Accept-Encoding" -> "gzip, deflate",
		"Accept-Language" -> "en-US,en;q=0.5",
		"Connection" -> "keep-alive",
		"Pragma" -> "no-cache",
		"User-Agent" -> "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0")

	val headers_4 = Map("Pragma" -> "no-cache")

    val uri1 = "http://detectportal.firefox.com/success.txt"
    val uri2 = "http://en-gb.appex-rf.msn.com/cgtile/v1"
    val uri3 = "http://192.168.99.100:32228"
    val uri4 = "http://finance.services.appex.bing.com/Market.svc/AppTileV2"
    val uri5 = "http://foodanddrink.tile.appex.bing.com/api/feed"

	val scn = scenario("RecordedSimulation")
		.exec(http("request_0")
			.get(uri3 + "/")
			.headers(headers_0))
		.pause(5)
		.exec(http("request_1")
			.get("/success.txt")
			.headers(headers_1))
		.pause(6)
		.exec(http("request_2")
			.get("/success.txt")
			.headers(headers_1))
		.pause(16)
		// getData
		.exec(http("request_3")
			.get("/success.txt")
			.headers(headers_1)
			.resources(http("request_4")
			.get(uri5 + "/?view-name=data&name=livetile&market=en-GB&version=2_0&format=xml")
			.headers(headers_4)
			.check(status.is(503)),
            http("request_5")
			.get(uri2 + "/EN-GB/News/today/4.xml?cgversion=v6")
			.headers(headers_4),
            http("request_6")
			.get(uri2 + "/en-GB/Sports/Today.xml?cgversion=v6")
			.headers(headers_4),
            http("request_7")
			.get(uri2 + "/en-GB/HealthAndFitness/Home.xml?cgversion=v6")
			.headers(headers_4),
            http("request_8")
			.get(uri2 + "/EN-GB/News/today/3.xml?cgversion=v6")
			.headers(headers_4),
            http("request_9")
			.get(uri2 + "/EN-GB/News/Today.xml?cgversion=v6")
			.headers(headers_4),
            http("request_10")
			.get(uri2 + "/EN-GB/News/today/2.xml?cgversion=v6")
			.headers(headers_4),
            http("request_11")
			.get(uri4 + "?symbols=&contentType=-1&tileType=0&locale=en-GB")
			.headers(headers_4)))

	setUp(scn.inject(atOnceUsers(1))).protocols(httpProtocol)
}