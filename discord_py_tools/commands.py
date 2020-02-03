import discord
from . import file_io, misc
from .file_io import log
from .misc import format_iterable

class Command: 
    func = None
    name = '' 
    description = '' 
    special_note = None
    groups = () 
    indefinite_args = () 
    required_args = () 
    optional_args = () 
    special_args_check = None

    def __init__(self, client, channel): 
        self.client = client
        self.channel = channel
        self.total_args = list(self.required_args) + ['[{}]'.format(arg) for arg in self.optional_args] 

        #log(self.total_args) 

        if self.indefinite_args: 
            self.total_args[-1] = '*{}'.format(self.total_args[-1]) 
        
        prefix = self.client.prefix(self.channel) 
        args_str = format_iterable(self.total_args, formatter=' {}', sep=' ') 
        self.syntax = prefix + self.name + args_str

    '''
    def __init__(self, func, name, description, indefinite_args, required_args, optional_args, special_args_check): 
        self.func = func
        self.name = name
        self.description = description
        self.indefinite_args = indefinite_args
        self.required_args = required_args
        self.optional_args = tuple(('[{}]'.format(arg) for arg in optional_args)) 
        self.total_args = list(self.required_args + self.optional_args) 

        if self.indefinite_args: 
            self.total_args[-1] = '*{}'.format(self.total_args[-1]) 
        
        args_str = format_iterable(self.total_args, formatter=' {}', sep=' ') 
        self.syntax = '(prefix)' + self.name + args_str
        
        self.special_args_check = special_args_check
    ''' 

    def help_embed(self): 
        embed = discord.Embed(title=self.name, type='rich', description=self.description) 

        embed.add_field(name='Usage', value='''`{}` 

`[` and `]` denote optional arguments; `*` denotes "indefinite" arguments (that is, you can put as many arguments as you want there) '''.format(self.syntax), inline=False) 

        if self.special_note is not None: 
            embed.add_field(name='Important note', value=self.special_note, inline=False) 
        
        groups_str = ttd_tools.format_iterable(self.groups) or None

        embed.add_field(name='Categories', value=groups_str) 

        '''
        embed.add_field(name='Usage - `[` and `]` denote optional arguments; `*` denotes "indefinite" arguments (that is, you can put as many arguments as you want there) ', value='`{}`'.format(self.syntax)) 
        ''' 

        return embed
    
    async def check_args(self, report, author, args): 
        valid = False

        if len(args) < len(self.required_args): 
            missing_args = self.required_args[len(args):] 
            missing_str = format_iterable(missing_args, formatter='`{}`') 

            report.add('{}, `{}` is missing arguments {}. '.format(author.mention, self.name, missing_str)) 
        elif not self.indefinite_args and len(args) > len(self.total_args): 
            report.add('{}, you gave too many arguments to `{}`; it only needs {}. '.format(author.mention, self.name, len(self.total_args))) 
        elif await self.__class__.special_args_check(self.client, report, author, *args): 
            valid = True
        
        return valid
    
    async def run(self, report, author, args): 
        #log(self.func) 
        #log(self.special_args_check) 

        if await self.check_args(report, author, args): 
            return await self.__class__.func(self.client, report, author, *args) 
        else: 
            report.add(self.help_embed()) 

''' 
async def default_special_args_check(report, author, args): 
    return True

def command(name, description, indefinite_args=False, required_args=(), optional_args=(), special_args_check=default_special_args_check): 
    def decorator(func): 
        return Command(func, name, description, indefinite_args, required_args, optional_args, special_args_check) 
    
    return decorator
''' 

def requires_owner(func): 
    async def arequiring_func(self, report, author, *args): 
        if author.id == self.owner_id: 
            return await func(self, report, author, *args) 
        else: 
            report.add('But it failed! ') 
    
    return arequiring_func
