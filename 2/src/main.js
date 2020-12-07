const { parse } = require('node-html-parser')
const fs = require('fs');
const request = require("async-request");

class Main
{

    constructor()
    {
        this._ROOT_URL = 'http://91.210.252.240/broken-links/'
        this._START_URL = this._ROOT_URL;

        this._VALID_LINKS_FILE_NAME = 'valid.txt';
        this._INVALID_LINKS_FILE_NAME = 'invalid.txt';

        this._urlsStack = [];
        this._validUrls = [];
        this._invalidUrls = [];
        this._vendorLinks = [ 'https://colorlib.com' ];
    }

    async execute()
    {
        this._urlsStack.push(this._START_URL);

        await this.checkUrl('');

        fs.writeFileSync(this._VALID_LINKS_FILE_NAME, JSON.stringify(this._validUrls));
        fs.writeFileSync(this._INVALID_LINKS_FILE_NAME, JSON.stringify(this._invalidUrls));
    }

    async checkUrl(link)
    {
        if (this._vendorLinks.includes(link))
        {
            return;
        }

        const url = this._ROOT_URL + link;

        if (this._isAlreadyVisited(url))
        {
            return;
        }

        try
        {
            var result = await request(url);

            if (result.statusCode < 200 || result.statusCode >= 300)
            {
                this._invalidUrls.push(url);
                return;
            }
        }
        catch (error)
        {
            this._invalidUrls.push(url);
            return;
        }

        this._validUrls.push(url);

        const document = parse(result.body);

        const elements = document.querySelectorAll('a');

        for (let i = 0; i < elements.length; i++)
        {
            const element = elements[i];

            if (!element.attributes.hasOwnProperty('href') || element.attributes.href.startsWith('#'))
            {
                return;
            }

            await this.checkUrl(element.attributes.href);
        }
    }

    _isAlreadyVisited(link)
    {
        return this._validUrls.find(url => { return url === link }) || this._invalidUrls.find(url => { return url === link })
    }
}


const main = new Main();

main.execute();
