[[!meta title="IRC"]]

Our IRC server is composed of two crucial parts. The first is the IRCd, or IRC
daemon. This piece is the server that everyone connects to and that controls
the basic chat functions, like having channels, nicknames, and generally
following the IRC server protocol ([RFC 2813][rfc2813]). The other parts of the
server are the IRC Services, which provides things like topic saving on
channels, auto-op lists, etc. These features aren't strictly necessary, but are
nice to have, and make the IRC server a lot more versatile and useful. Without
services, the IRC server would not have auto-ops, be able to reserve nicknames
for users, or keep persistent channel topics after restarts, all things we want
to do.

## IRCd (inspIRCd)

We currently use [inspIRCd][inspircd] as our IRCd of choice. It was chosen to
replace [ircd-hybrid][ircd-hybrid] (our previous non-puppeted IRCd) since it is
generally newer (better maintained/more updates), and has some modules that we
like, such as sqloper, which loads opers from a SQL database, so that no local
databases need to be used (easier to bring up a new VM with Puppet).  It also
contains built-in SSL support (with GnuTLS) in the Debian package, unlike
ircd-hybrid, which doesn't have SSL compiled in due to licensing issues.

## IRC Services (anope)

[Anope][anope] is our IRC services of choice and is used to provide some nice
features, like nickname retention, registration of channels, topic saving on
channels, and auto-op/access lists. We use a pretty simple subset of the
features that anope offers and there are many more, especially with anope's
[suite of extra modules][anope-modules]. Overall though, we like to keep it
simple and don't need many of the fancier features and modules out there,
especially since we have a pretty small IRC server with not many channels.

## Puppeting IRC

Puppeting IRC is definitely not an easy process, as every IRCd and services
package I looked at were quite complicated, even the ones that advertized
themselves as being "simpler." The config files are long and contain many
options and terminology that is complicated, especially if not used to all the
terms around IRC.


[rfc2813]: https://tools.ietf.org/html/rfc2813
[inspircd]: http://www.inspircd.org
[ircd-hybrid]: http://www.ircd-hybrid.org
[anope]: https://www.anope.org
[anope-modules]: https://modules.anope.org
