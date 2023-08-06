from twisted.internet import reactor, protocol


class VolcanoTwistedFactory(protocol.ClientFactory):
    nb_attempts = 3
    nb_attempts_made = 0
    reconnect_pause = 3.0
    log = None
    client = None

    def clientConnectionFailed(self, connector, reason):
        self.nb_attempts_made += 1
        if self.nb_attempts_made < self.nb_attempts:
            if self.log:
                self.log.warn(
                    'Connection to Volcano {} failed (attempt {}/{}): {}. Try again in {} secs...'.format(
                        connector.getDestination(),
                        self.nb_attempts_made,
                        self.nb_attempts,
                        reason.getErrorMessage(),
                        self.reconnect_pause))
            reactor.callLater(self.reconnect_pause, connector.connect)  # pylint: disable=no-member
        else:
            if self.log:
                self.log.error('Connection to Volcano {} failed (attempt {}/{}): {}. Abort!'.format(
                    connector.getDestination(),
                    self.nb_attempts_made,
                    self.nb_attempts,
                    reason.getErrorMessage()))
            reactor.stop()      # pylint: disable=no-member

    def clientConnectionLost(self, connector, reason):
        if self.log:
            self.log.error('Connection to volcano-core lost: {}'.format(reason.getErrorMessage()))
        if reactor.running:     # pylint: disable=no-member
            reactor.stop()      # pylint: disable=no-member

    def buildProtocol(self, addr):
        if self.client:
            return self.client
        else:
            return super().buildProtocol(addr)
