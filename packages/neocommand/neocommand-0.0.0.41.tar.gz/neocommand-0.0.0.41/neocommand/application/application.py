import intermake
from neocommand.data.core import Core
from neocommand.application import help, coercers


class Application( intermake.Application ):
    INSTANCE = None
    
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.core = Core( self )
    
    def on_create_controller( self, mode: str ):
        controller = super().on_create_controller(mode)
        coercers.init( controller.coercers )
        return controller
        


Application.INSTANCE = Application( name = "neocommand" )
help.init( Application.INSTANCE )
app = Application.INSTANCE