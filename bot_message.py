import db_handler as db
import random
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

langs = {
    'English' : {        
        'adjustSettings': "Adjust your settings",
        'AllianceCreated': 'Alliance info created!',
        'AllianceUpdated': 'Alliance info updated!',
        'AllianceRosterUpdate': 'Alliance roster updated!',
        'AllianceUnknown': 'Alliance not found!',
        'AtkListUpdated': 'Guild atklist updated!',
        'BattleNotif': 'Battle is coming. Equip your weapon and get your orders!',
        'ChoseTop': "Choose the top stats",
        'DefListUpdated': 'Guild deflist updated!',
        'EncounterSent': 'Thanks for sending monsters.',
        'EncounterTooOld': 'Sorry, your encounter is too old (has already finished).',
        'EmptyMessage': 'Write something, dude',
        'ErrorParsing': 'Error Parsing your message',
        'OrderAcepted': 'Your order is ready. Clic "send all" button in a private chat.',
        'GuildUnknown': 'Guild not found!\nForward your /guild TAG first',
        'GuildCreated': 'Guild info created!',
        'GuildUpdated': 'Guild info updated!',
        'LocationKnown': "Already known location. Thanks!!!",
        'LocNotFound': "Location not found",
        'LocDis': "Location disabled",
        'NewLocation': "That's a new one. Thanks!!!",
        'NoGuild': 'Error 404 Guild not found',
        'NoPriviledges': 'You do not have privileges to go there.',
        'NoTargetError': 'Set target first',
        'NoTierError': 'Select a tier for the order',
        'NoOrders': " hasn't set orders yet",
        'NothingFound': 'Nothing found yet',
        'NoSpam': 'Please avoid spamming me!',
        'OrderNotif': ' just set the orders. Check the ⚜️ Order button',
        'OrderSaved': 'Order Saved',
        'PlayerUpdated': 'Player info updated!',
        'RosterUpdated': 'Guild roster updated!',
        'ReportOK': 'Thanks for sending report',
        'SettingOverview': "Setting Overview",  
        'UserNotRegister': "I don't talk to strangers.\nSend me your cellphone number ☎️ to suscribe to alerts.\n\n /subscribe ########",          
        'UnknownCWMsg': 'ChatWars Message not recognized!',        
        'Stock': 'Generating deposit msg!',        
        'Welcome': "Welcome back",
        'WelcomeAdmin': "Welcome Admin",
        'WelcomeCommander': "Welcome Commander",      
        'AddedAlert': "✔️ Alert enabled!!!",      
        'RemoveAlert': "❌ Alert disabled!!!",
        'RemovePhone': "❌ Deleted!!!",
        'Subscribed': "You are now subscribed!!!", 
        '5ta': "⚠️⚠️ Modulo en 5ta y 42 ⚠️⚠️!!!", 
        'WrongNumber': "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n Your cellphone number must be 8-10  digits long and no string or symbols!!!"      
    },
    'Spanish' : {        
        'adjustSettings': "Ajusta tus configuraciones",
        'AllianceCreated': 'Información de Alianza creada!',
        'AllianceUpdated': 'Información de Alianza actualizada!',
        'AllianceRosterUpdate': 'Lista de la Alianza actualizada!',
        'AllianceUnknown': 'Alianza no encontrada!',
        'AtkListUpdated': 'Se actualizó la lista atk del gremio!',
        'BattleNotif': 'La batalla se acerca. Equipa tu arma y recibe tus órdenes!',
        'ChoseTop': "Elige las mejores estadísticas",
        'DefListUpdated': 'Lista de def del gremio actualizado!',
        'EncounterSent': 'Gracias por enviar monstruos.',
        'EncounterTooOld': 'Lo sentimos, tu encuentro es demasiado viejo (ya ha terminado).',
        'EmptyMessage': 'Escribe algo, amigo',
        'ErrorParsing': 'Error al analizar tu mensaje',
        'OrderAcepted': 'Tu orden está lista. Haga clic en el botón "enviar todo" en un chat privado.',
        'GuildUnknown': '¡No se encontró el gremio!\nEnvía primero tu ETIQUETA /guild',
        'GuildCreated': 'Información del gremio creada!',
        'GuildUpdated': 'Información del gremio actualizada!',
        'LocationKnown': "Ubicación ya conocida. Gracias!!!",
        'LocNotFound': "Ubicación no encontrada",
        'LocDis': "Ubicación deshabilitada",
        'NewLocation': "Esa es una nueva. Gracias!!!",
        'NoGuild': 'Error 404 Gremio no encontrado',
        'NoPriviledges': 'No tienes privilegios para ir allí.',
        'NoTargetError': 'Establecer objetivo primero',
        'NoTierError': 'Seleccione un Tier para la orden',
        'NoOrders': " Aún no se han establecido pedidos",
        'NothingFound': 'Aún no se ha encontrado nada.',
        'NoSpam': 'Por favor evite enviarme spam!',
        'OrderNotif': ' Ordenes establecidas. Verifique el botón ⚜️ Order',
        'OrderSaved': 'Orden Guardada',
        'PlayerUpdated': 'Información del jugador Actualizada!',
        'RosterUpdated': 'Lista del gremio actualizada!',
        'ReportOK': 'Gracias por enviar el reporte',
        'SettingOverview': "Descripción general de la configuración",  
        'UserNotRegister': "Yo no hablo con extraños.\nEnviame tu numero ☎️ para suscribirte a las alertas\n\n /subscribe ########",          
        'UnknownCWMsg': 'Mensaje de ChatWars no reconocido!',        
        'Stock': 'Generando mensaje de deposito!',        
        'Welcome': "Bienvenido de vuelta",
        'WelcomeAdmin': "Bienvenido Admin",
        'WelcomeCommander': "Bienvenido Commander",      
        'AddedAlert': "✔️ Alerta habilitada!!!",      
        'RemoveAlert': "❌ Alerta deshabilitada!!!",      
        'RemovePhone': "❌ Eliminado!!!",      
        'Subscribed': "Usted esta suscrito!!!",
        '5ta': "⚠️⚠️ Modulo en 5ta y 42 ⚠️⚠️!!!",
        'WrongNumber': "⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️\n Su numero debe ser de 8-10 digitos y sin caracteres o simbolos!!!"       
    }
}

def get_user_alert_status_prod(tgid=None):
    res = "🔊 Estas son sus alertas activas:\n\n"
    # Settings4User todos los settings activos por el usuario
    settings_user = db.get_user_alerts(uid=tgid)
    if settings_user:
        for a in settings_user:
            settings = db.get_setting_alert(settings_user=a,kind='alert')
            if settings:
                for i in settings:
                    res += '- {} \n'.format(i.name)
        res += '\n Seleccione sobre que desea ser notificado. \n'
        return res
    else:
        res += '----No tiene alertas activas---- \n\n'
        res += 'Seleccione sobre que desea ser notificado. \n'
        return res
def get_user_alert_status_url(tgid=None):
    res = "🔊 Estas son sus alertas activas:\n\n"
    # Settings4User todos los settings activos por el usuario
    settings_user = db.get_user_alerts(uid=tgid)
    if settings_user:
        for a in settings_user:
            settings = db.get_setting_alert(settings_user=a,kind='url')
            if settings:
                for i in settings:
                    res += '- {} \n'.format(i.name)
        res += '\n Seleccione sobre que desea ser notificado. \n'
        return res
    else:
        res += '----No tiene alertas activas---- \n\n'
        res += 'Seleccione sobre que desea ser notificado. \n'
        return res

    
def get_alert_options_btn_url(tgid=None):
    settings_user = db.get_user_alerts(uid=tgid)
    if settings_user:
        btn = InlineKeyboardMarkup(row_width=2)
        for sets_u in settings_user:
            settings = db.get_setting_alert(settings_user=sets_u, kind='url')
            
            if settings:
                for sets in settings:
                    if sets.name == sets_u.setting_id:
                        btn.insert(InlineKeyboardButton("❌ "+sets.name, callback_data=sets.name))
                    break
        settings = db.get_setting_alert_left(settings_user=settings_user, kind='url')
        if settings:
            for sets in settings:
                if sets.name == sets_u.setting_id:
                    break
                else:
                    btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))
    else:
        settings = db.get_setting_alert(kind='url')
        if settings:
            for sets in settings:
                btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))
                
    
    return btn       
def get_alert_options_btn_prod(tgid=None):
    settings_user = db.get_user_alerts(uid=tgid)
    btn = InlineKeyboardMarkup(row_width=2)
    if settings_user:
        for sets_u in settings_user:
            settings = db.get_setting_alert(settings_user=sets_u, kind='alert')
            
            if settings:
                for sets in settings:
                    if sets.name == sets_u.setting_id:
                        btn.insert(InlineKeyboardButton("❌ "+sets.name, callback_data=sets.name))
                    break
        settings = db.get_setting_alert_left(settings_user=settings_user, kind='alert')
        if settings:
            for sets in settings:
                if sets.name == sets_u.setting_id:
                    break
                else:
                    btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))
    else:
        settings = db.get_setting_alert(kind='alert')
        if settings:
            for sets in settings:
                btn.insert(InlineKeyboardButton("✅ "+sets.name, callback_data=sets.name))
    
    return btn       
        
    

                    
            # for sets,sets_u in [(sets,sets_u) for sets in settings for sets_u in settings_user]:
 
    

def get_help():
    res = '<code> creador:</code>  @mr_charlie93 \n\n'
    res += '<b>comandos utiles:</b> <code>/help, </code>'
    return res


def get_static_message(message_key, ulang='English'):
    if not ulang in langs.keys():
        ulang = 'Spanish'
    if message_key in langs[ulang].keys():
        return langs[ulang][message_key]
    return message_key


def get_settings_menu(message):
    res = "⚙️ " + get_static_message('adjustSettings', ulang='Spanish') + "\n\n"
    res +="Eliminar telefono del sistema /removeme"
    return res





