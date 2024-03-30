# Discord Data Package Analyzer

This repository is made to analyze [Discord Data Package](https://support.discord.com/hc/en-us/articles/360004957991-Your-Discord-Data-Package).

## Motivation

I was destroyed by some random Korean person recently, because he spreaded my discord messages without any pre/post-context.
So I decided to remove all my discord messages and requested to the Discord Privacy Team.

At first, they said my inquiry is not in the right place.
After I complained to them with providing several screenshots on Discord FAQ, they responded the following message;

> Hi there,
>
> Thank you for reaching out to us.
>
> We don't offer the ability to delete your messages in bulk right now.
>
> *(So if you don't offer to bulk deleting messages.. How can we ensure that our personal data is deleted by our request in a reasonable time, considering the amount of messages in Discord is enormous?)*
>
> We try to balance the interests other users have in a conversation, as well as the ability for us to provide the service as a whole. Discord is a communications service and its users have a legitimate interest in having access to content sent to them. Consistent with GDPR, Discord balances the privacy interests of the user against the interests other users have in a conversation and the ability for us to provide the service as a whole. Because of how Discord works, content is sent to other users, and those users rely on having access to that content. If a given text channel were suddenly missing important context, it would be confusing to other users or possibly mislead those users about what happened in that conversation.
>
> *(Are you saying our privacy data is less important than making a reading context makes sense?)*
>
> However, we understand that there may be reasons to delete or edit individual messages. To support this, we offer users the ability to edit or delete their own messages; and as long as you retain access to your Discord account you may delete or edit messages as you see fit. You can delete content you sent in a Text Channel by right clicking on the message and selecting "Delete Message." You can also access this feature by placing your mouse cursor over the message and clicking on the "..." to display the "Delete Message" option. If you hold the "Shift" key while hovering your cursor over a message and select the delete icon (represented by a small red trash can), you can bypass the deletion confirmation screen and more quickly delete content.
> 
> *(Makes sense, but I have 60k+ messages and I don't want to delete them by clicking icons manually..)*
>
> Of course, we also want to respect our users' privacy — that's why we anonymize messages upon account deletion. We remove everything including username, email address, and IPs in our systems, so there is no personal data left and even we at Discord wouldn't be able to tell who wrote the message. If a user comes upon the conversation after deletion, all they would see is that a deleted user wrote the messages.
>
> *(Some messages still violates personal safety and privacy because of its contents without information of message sender..)*
>
> For sensitive or personal content located in spaces that you cannot access, we suggest requesting your Discord Data Package that contains all the messages, images, or files that you have sent from your account, including messages you have sent in servers that you can no longer access. This article explains how to Request a Copy of your Data. And for more information regarding the kind of information we include in your data package, check out this article: Your Discord Data Package.
>
> Your Data Package should help you identify any messages, images, or files that you would like deleted in spaces that you currently cannot access. If you provide us with a list of the Message IDs and the corresponding channel IDs that contain personal information, we will gladly work to delete the messages you identify.
>
> We hope this information has been helpful. 
>
> Sincerely,
> Discord Privacy Team

And I decided to make a program to export all message IDs and corresponding channel IDs automatically.
I will make this git repo to public after I succeed to delete all my messages, in case anyone else needs to do the same thing.

## How to use

1. Clone this git repository in your local machine.

2. Unzip your Discord data package.

3. Run following code.

    ```python
    # This importing path might change if your cwd is different
    from unpackager import DiscordPackage

    package = DiscordPackage("YOUR_DISCORD_PACKAGE_PATH")

    # ... do whatever you can
    ```

For available public methods, please read the `unpackager.py`.
