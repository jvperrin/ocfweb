[[!meta title="IRC"]]

Our IRC server is composed of two crucial parts:

1. The IRCd, or IRC daemon. This piece is the server that everyone connects to
   and that controls the basic chat functions, like having channels, nicknames,
   and generally following the IRC server protocol.

2. IRC Services, which provides things like channel topic saving when the
   server reboots, auto-op lists, channel permission controls, etc. These
   features aren't strictly necessary, but are nice to have, and make the IRC
   server a lot more versatile and useful.  Without services, the IRC server
   would not have auto-ops, be able to reserve nicknames for users, or keep
   persistent channel topics after restarts, all things we want to do.


## IRCd (inspIRCd)

We currently use [inspIRCd][inspircd] as our IRCd of choice. It was chosen to
replace [ircd-hybrid][ircd-hybrid] (our previous non-puppeted IRCd) since it is
generally newer, better maintained, gets more updates, and has some modules
that we like. [These modules][inspircd-modules] include sqloper, which loads
opers from a SQL database, so that no local databases need to be used (easier
to bring up a new VM with Puppet). It also contains built-in SSL support with
GnuTLS in the Debian package, unlike ircd-hybrid, which doesn't have SSL
compiled in due to licensing issues. Since we only support using SSL to connect
to our IRC server, having well-maintained SSL support is important.

[inspircd]: http://www.inspircd.org
[ircd-hybrid]: http://www.ircd-hybrid.org
[inspircd-modules]: https://wiki.inspircd.org/2.0/Modules


## IRC Services (anope)

[Anope][anope] provides our IRC Services of choice and provides some nice
features, like nickname retention, registration of channels, topic saving on
channels, and auto-op/access lists. We use a pretty simple subset of the
features that Anope offers, especially with Anope's [suite of extra
modules][anope-modules]. Overall though, we like to keep it simple since it's
easier to maintain, less likely to break in the future, and because we don't
need many of the fancier features and modules out there designed for larger IRC
servers.

[anope]: https://www.anope.org
[anope-modules]: https://modules.anope.org


## Puppeting IRC

Puppeting IRC is definitely not an easy process, as every IRCd and services
package has lots of configuration options, even the ones that advertized
themselves as being "simpler." The config files are long and contain many
options and terminology that is complicated, especially if not used to all the
terms around IRC. In total the config files for Anope contained over 6000 lines
of config and associated comments to sift through.
