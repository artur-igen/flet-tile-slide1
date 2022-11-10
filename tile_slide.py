#minden ok, szebb keverést
"""
Tile Slide game by Szemán Artúr
Ver: 0.0  :)

Where to go:
- picture instead of numbers
- more attractive design
- settings (menu)
- sound effects?
- mixing with gesture effect?
- POSSIBILITY OF NEW GAME!! :D
- click event called when dragging begins (on_up event or mouse event?)
"""
import flet
from flet import (Container, Draggable, DragTarget, Page, Row, Text, alignment, 
    colors, border, ContainerTapEvent, ElevatedButton, AlertDialog)
import random
import time

GAME_SIZE = (5, 5)     #count of tiles (horizontal, vertical)
TILE_SIZE = (50, 50)   #size of tiles (horizontal, vertical)
DRAG_GROUP = "TILESLIDE"

class Tile():
    def __init__(self, orig_x, orig_y, is_tile, drag_cont) -> None:
        self.orig_coord = (orig_x, orig_y)
        self.act_coord = self.orig_coord
        self.is_tile = is_tile #True: tile, False: the hole
        self.drag_cont = drag_cont
        drag_cont.data = self


def main(page: Page):

    page.title = "Tile Slide Game"
    page.spacing = 0
    page.window_height = 400
    page.window_width = 400

    def is_done() -> bool:
        """
        Is everything in place?
        """
        for r, tiles_row in enumerate(tiles):
            for c, t in enumerate(tiles_row):
                if t.act_coord != t.orig_coord:
                    return False

        return True        


    def container2tile(container):
        """
        Which tile has the container. For container onclick. For now not used     
        """    
        for r, tiles_row in enumerate(tiles):
            for c, t in enumerate(tiles_row):
                if t.drag_cont.content == container:
                    return r, c, t

        return False        

    def swap(src_tile: Tile, trg_tile: Tile):
        """
        Swaps a tile with the hole (or two tiles: Why?)
        """
        #print(src_tile.act_coord, trg_tile.act_coord)
        trg_control = trg_tile.drag_cont
        src_control = src_tile.drag_cont
        
        #they are neighbours
        if ( ( src_tile.act_coord[0] == trg_tile.act_coord[0] and 
               abs(src_tile.act_coord[1] - trg_tile.act_coord[1] ) == 1)
            or ( src_tile.act_coord[1] == trg_tile.act_coord[1] and 
               abs(src_tile.act_coord[0] - trg_tile.act_coord[0] ) == 1)
        ):

            src_row: Row = pagerows[src_tile.act_coord[1]]
            trg_row: Row = pagerows[trg_tile.act_coord[1]]

            src_row.controls[src_tile.act_coord[0]] = trg_control    
            trg_row.controls[trg_tile.act_coord[0]] = src_control
            tiles[ src_tile.act_coord[1] ] [src_tile.act_coord[0]] = trg_tile
            tiles[ trg_tile.act_coord[1] ] [trg_tile.act_coord[0]] = src_tile
            src_tile.act_coord, trg_tile.act_coord = trg_tile.act_coord, src_tile.act_coord

            page.update()

        else:
            pass

    def tile_click(e: ContainerTapEvent):  #todo: click event called when dragging begins
        pass
        #print("tile_click", container2tile(e.control) ) 

    def drag_accept(e: DragTarget):
        # get draggable (source) control by its ID
        src_control = page.get_control(e.src_id)
        src_tile: Tile = src_control.data
        trg_control = e.control
        trg_tile: Tile = trg_control.data

        swap(src_tile, trg_tile)


    def game_item(is_tile, text):
        """
        Makes the dragging control and the visual controls in it
        """
        if is_tile:
            bgcolor = colors.CYAN_200
            content  = text
        else:
            bgcolor = "white"
            content  = ":)"

        ret = {True: Draggable, False: DragTarget } [is_tile] (
                        group = DRAG_GROUP,
                        content = Container(
                            width=TILE_SIZE[0],
                            height=TILE_SIZE[0],
                            bgcolor=bgcolor,
                            border=border.all(width=1, color="black"),
                            content=Text(content, size=20),
                            alignment=alignment.center,                            
                        )    
        )

        if is_tile:
            ret.content.on_click = tile_click
        else:    
            ret.on_accept = drag_accept

        return ret

    def game_init():
        cnt = 0
        for r in range(GAME_SIZE[1]):
            row = Row(spacing=0)
            tiles_row = []
            for c in range(GAME_SIZE[0]):
                cnt += 1   
                is_tile = c < GAME_SIZE[0] - 1 or r < GAME_SIZE[1] - 1       
                row.controls.append(
                    drag_cont := game_item(is_tile, str(cnt))
                )
                tiles_row.append( Tile(c, r, is_tile, drag_cont) )
            page.add(row)
            tiles.append(tiles_row)    
            pagerows.append(row)


    def btn_check_click(e):
        dlg = AlertDialog(
            title = Text( "Clever!" if is_done() else "Keep doing it"),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def btn_mix_click(e):
        def get_hole():
            for r, tiles_row in enumerate(tiles):
                for c, tile in enumerate(tiles_row):
                    if not tile.is_tile:
                        return r, c, tiles[r][c]
            return False

        btn_mix.disabled = True
        try:
            r,c, _ = get_hole()                

            for i in range(10):
                while True:
                    direction = random.choice("lrud")
                    r1, c1 = r, c

                    if direction == "l":
                        c1 -= 1
                    elif direction == "r":
                        c1 += 1
                    elif direction == "u":
                        r1 -= 1
                    else:
                        r1 += 1
                        c1 = c

                    if 0 <= c1 < len( tiles[0] ) and  0 <= r1 < len(tiles):
                        break

                swap( tiles[r][c], tiles[r1][c1])
                r, c = r1, c1

                time.sleep(0.1)   
        finally:
            btn_mix.disabled = False         

        btn_mix.text = "Mix more"    
        page.update()


    game_init()
    page.add(
        Container(height=3),
        btn_check := ElevatedButton("Check", on_click = btn_check_click),
        Container(height=3),
        btn_mix := ElevatedButton("Mix", on_click = btn_mix_click),
    )


tiles = []
pagerows = [] #todo: getting the parent row via its control

flet.app(target=main)