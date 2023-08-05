def check_for_updates():
    from os import path
    from dline.utils.globals import gc

    if not path.exists(".git"):
        print(gc.term.red("Error: client not started from repo location! Cancelling..."))
        print(gc.term.yellow("You must start the client from its folder to get automatic updates. \n"))
        return

    try:# git pull at start as to automatically update to master repo
        from subprocess import Popen,PIPE
        print(gc.term.green + "Checking for updates..." + gc.term.normal)
        process = Popen(["git", "pull", "--force"], stdout=PIPE)
        output = process.communicate()[0].decode('utf-8').strip()

        if "Already up to date" not in output:
            # print(gc.term.yellow("Updates downloaded! Please restart."))
            print("\n \n")
            # This quit() call is breaking the client on MacOS and Linux Mint
            # The if statement above is being triggered, even when the output IS
            # "Already up to date". Why is this happening?
            # quit()
        else:
            print("Already up to date!" + "\n")
    except KeyboardInterrupt: print("Call to cancel update received, skipping.")
    except SystemExit: pass
    except OSError: # (file not found)
        # They must not have git installed, no automatic updates for them!
        print(gc.term.red + "Error fetching automatic updates! Do you \
              have git installed?" + gc.term.normal)
    except:
        print(gc.term.red + "Unkown error occurred during retrieval \
              of updates." + gc.term.normal)
