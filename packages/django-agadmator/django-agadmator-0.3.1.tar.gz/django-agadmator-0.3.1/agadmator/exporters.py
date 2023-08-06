import chess
from chess.pgn import StringExporter


class FenExporter(StringExporter):

    def __init__(self):
        super().__init__(comments=False, headers=False, variations=False, columns=None)
        self.positions = []

    def visit_header(self, tagname, tagvalue):
        pass

    def visit_move(self, board, move):
        self.positions.append(board.fen())

    def result(self):
        return self.positions


class MarkupExporter(StringExporter):

    def __init__(self):
        super().__init__(columns=None, headers=False, comments=False, variations=False)

    def visit_move(self, board, move):
        if self.variations or not self.variation_depth:
            # Write the move number.
            if board.turn == chess.WHITE:

                self.write_token(str(board.fullmove_number) + ". ")
            elif self.force_movenumber:
                self.write_token(str(board.fullmove_number) + "... ")

            offset = -1 if board.turn == chess.WHITE else 0
            n = 2 * board.fullmove_number + offset
            # Write the SAN.
            self.write_token(f'<span class="cp" id="p-{n}" data-i="{n}">{board.san(move)}</span> ')
            self.force_movenumber = False

    def visit_result(self, result):
        pass