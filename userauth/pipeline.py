# # userauth/pipeline.py
# import logging

# logger = logging.getLogger(__name__)

# def save_email(backend, user, response, *args, **kwargs):
#     logger.debug('Entered save_email pipeline function')  # Log entry to the function
    
#     # Log the entire response to check if email is present
#     logger.debug(f'OAuth Response: {response}')
    
#     email = response.get('email')
    
#     if email:
#         user.email = email
#         user.save()
#         logger.debug(f'Email {email} saved for user {user}')
#     else:
#         logger.warning('Email not found in OAuth response')
    
#     logger.debug('Exiting save_email pipeline function')  # Log exit from the function
