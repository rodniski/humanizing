# Examples

Before/after pairs. Each "before" is clean at the word level — no "delve", no em-dash flood — and still reads generated. The fixes are structural.

## Chat answer

**Before**

> I looked into the login timeouts. First I checked the application logs, then the load balancer config, and then the database connection pool. As experienced engineers often say, it's usually the simplest thing. In the end, the issue turned out to be the pool size. Ultimately, this shows how small configuration details can have a big impact on reliability.

**After**

> Login times out because the DB pool caps at 10 connections (`config/db.go:42`). I raised it to 50 and p99 dropped from 8.1 s to 240 ms. Not checked yet: whether the cache layer hides the same limit under real traffic.

Rules: 4 (conclusion first), 2 (file, line, numbers instead of "experienced engineers"), 1 (moral cut), 5 (open end stated).

## PR description

**Before**

> ## Summary
> This PR improves the reliability of the notification system.
> ## Changes
> - Refactored the retry logic
> - Updated the queue configuration
> - Added tests
> ## Impact
> These changes make notifications more robust and ensure a better experience for users.

**After**

> Push notifications were dropped whenever APNs returned 429, because the retry ran once with no backoff. Retries now back off exponentially (max 5, `retry.go`), and the queue keeps failed jobs for 24 h instead of discarding them.
>
> Tested against a mocked 429 storm. Not tested on Android/FCM, which uses a different path.

Rules: 6 (the three-heading template collapses into what matters), 2 (429, APNs, max 5, 24 h), 1 (the "Impact" moral disappears), 5 (FCM gap stated).

## Documentation

**Before**

> Authentication is a crucial part of any modern application. In this guide, we will walk through the process of setting up authentication step by step. First, we will install the dependencies. Then, we will configure the provider. Finally, we will test the login flow. By the end, you will have a solid understanding of how authentication works.

**After**

> To add login, install `auth-kit`, set `AUTH_ISSUER` and `AUTH_CLIENT_ID`, and call `requireUser()` in any loader that needs a session. The rest of this page covers the provider settings and what to do when the callback fails.

Rules: 1 and 4 (no preamble, no promised takeaway; the reader gets the answer in the first sentence), 2 (real names), 7 (written to someone who wants login working).

## Email

**Before**

> I hope this message finds you well. I wanted to reach out regarding the timeline for the project. After careful consideration of various factors, we believe it may be beneficial to explore adjusting our delivery date. We remain committed to delivering a high-quality result and appreciate your understanding.

**After**

> We'll miss the 14 Nov date. The payment provider's sandbox was down for nine days and we can't certify without it. New estimate is 28 Nov; I'll confirm on Friday once their support answers.

Rules: 4 (the news first), 3 (plain "we'll miss"), 2 (dates, the cause), 5 (estimate pending confirmation, said so).

## Fiction

**Before**

> Maria stood at the edge of the pier as the sun sank low. Her chest tightened with every wave that broke against the wooden posts, the salt air carrying memories of her father. She had spent years running from this place. But now, watching the light fade, she finally understood: home was never a place. It was the people who had loved her, and the courage to return.

**After**

> The pier had been repainted, which made her angry before she knew why. Her father had hated that green. She told the man at the bait shop she was only passing through, and that was a lie too, though not the one he thought.
>
> Two winters earlier, she had sold his boat to a dentist from Porto Alegre.

Rules: 1 and fiction (no lesson stated), 3 (anger named, not a tightening chest), 2 (green paint, bait shop, Porto Alegre), fiction/time (the jump back two winters delays the real disclosure), 5 (the lie stays unexplained).

## Over-correction

**Before (over-humanized)**

> Okay so. Login's broken. Pool's tiny, honestly. Bumped it. Faster now, I think? Who knows.

This trades AI tidiness for performed casualness and invented doubt. The fixed chat answer above is the target: plain, specific, ordered, and open only where something is actually unknown.
