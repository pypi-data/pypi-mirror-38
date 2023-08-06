from plover_retro_case.change_case import change_case

def retro_case(ctx, cmdline):
    action = ctx.copy_last_action()
    # {:retro_case:capPrev:capThis:delimiter?}
    args = cmdline.split(':')


    try:
        capPrev = args[0] == 'true'
    except IndexError:
        return action

    try:
        capThis = args[1] == 'true'
    except IndexError:
        return action

    try:
        delim = args[2]
    except IndexError:
        delim = ''

    action = ctx.copy_last_action()

    last_words = ctx.last_words(count=2)

    action.text = change_case(last_words, capPrev, capThis, delim )
    action.prev_replace = "".join(last_words)
    action.prev_attach = True
    action.word = None

    return action

